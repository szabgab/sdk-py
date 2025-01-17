# -*- coding: utf-8 -*-
#
#   DIM-SDK : Decentralized Instant Messaging Software Development Kit
#
#                                Written in 2020 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2020 Albert Moky
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ==============================================================================

from typing import Optional

from mkm.crypto import json_encode, json_decode, utf8_encode, utf8_decode

from dimp import ID
from dimp import Content, Command
from dimp import InstantMessage, SecureMessage, ReliableMessage
from dimp import Packer

from .helper import TwinsHelper


class MessagePacker(TwinsHelper, Packer):

    # Override
    def overt_group(self, content: Content) -> Optional[ID]:
        group = content.group
        if group is not None:
            if group.is_broadcast:
                # broadcast message is always overt
                return group
            if isinstance(content, Command):
                # group command should be sent to each member directly, so
                # don't expose group ID
                return None
            return group

    #
    #   InstantMessage -> SecureMessage -> ReliableMessage -> Data
    #

    # Override
    def encrypt_message(self, msg: InstantMessage) -> Optional[SecureMessage]:
        messenger = self.messenger
        # check message delegate
        if msg.delegate is None:
            msg.delegate = messenger

        sender = msg.sender
        receiver = msg.receiver
        # if 'group' exists and the 'receiver' is a group ID,
        # they must be equal

        # NOTICE: while sending group message, don't split it before encrypting.
        #         this means you could set group ID into message content, but
        #         keep the "receiver" to be the group ID;
        #         after encrypted (and signed), you could split the message
        #         with group members before sending out, or just send it directly
        #         to the group assistant to let it split messages for you!
        #    BUT,
        #         if you don't want to share the symmetric key with other members,
        #         you could split it (set group ID into message content and
        #         set contact ID to the "receiver") before encrypting, this usually
        #         for sending group command to assistant bot, which should not
        #         share the symmetric key (group msg key) with other members.

        # 1. get symmetric key
        group = messenger.overt_group(content=msg.content)
        if group is None:
            # personal message or (group) command
            password = messenger.cipher_key(sender=sender, receiver=receiver, generate=True)
            assert password is not None, 'failed to get msg key: %s -> %s' % (sender, receiver)
        else:
            # group message (excludes group command)
            password = messenger.cipher_key(sender=sender, receiver=group, generate=True)
            assert password is not None, 'failed to get group msg key: %s -> %s' % (sender, group)

        # 2. encrypt 'content' to 'data' for receiver/group members
        if receiver.is_group:
            # group message
            facebook = self.facebook
            grp = facebook.group(identifier=receiver)
            if grp is None:
                # group not ready
                # TODO: suspend this message for waiting group's meta
                return None
            members = grp.members
            if members is None or len(members) == 0:
                # group members not found
                # TODO: suspend this message for waiting group's membership
                return None
            s_msg = msg.encrypt(password=password, members=grp.members)
        else:
            # personal message (or split group message)
            s_msg = msg.encrypt(password=password)
        if s_msg is None:
            # public key for encryption not found
            # TODO: suspend this message for waiting receiver's meta
            return None

        # overt group ID
        if group is not None and receiver != group:
            # NOTICE: this help the receiver knows the group ID
            #         when the group message separated to multi-messages,
            #         if don't want the others know you are the group members,
            #         remove it.
            s_msg.envelope.group = group

        # NOTICE: copy content type to envelope
        #         this help the intermediate nodes to recognize message type
        s_msg.envelope.type = msg.content.type

        # OK
        return s_msg

    def sign_message(self, msg: SecureMessage) -> ReliableMessage:
        # check message delegate
        if msg.delegate is None:
            msg.delegate = self.messenger
        assert msg.data is not None, 'message data cannot be empty: %s' % msg
        # sign 'data' by sender
        return msg.sign()

    def serialize_message(self, msg: ReliableMessage) -> bytes:
        js = json_encode(obj=msg.dictionary)
        return utf8_encode(string=js)

    #
    #   Data -> ReliableMessage -> SecureMessage -> InstantMessage
    #

    def deserialize_message(self, data: bytes) -> Optional[ReliableMessage]:
        js = utf8_decode(data=data)
        dictionary = json_decode(string=js)
        # TODO: translate short keys
        #       'S' -> 'sender'
        #       'R' -> 'receiver'
        #       'W' -> 'time'
        #       'T' -> 'type'
        #       'G' -> 'group'
        #       ------------------
        #       'D' -> 'data'
        #       'V' -> 'signature'
        #       'K' -> 'key'
        #       ------------------
        #       'M' -> 'meta'
        return ReliableMessage.parse(msg=dictionary)

    def verify_message(self, msg: ReliableMessage) -> Optional[SecureMessage]:
        # TODO: make sure meta exists before verifying message
        facebook = self.facebook
        sender = msg.sender
        # [Meta Protocol]
        meta = msg.meta
        if meta is not None:
            facebook.save_meta(meta=meta, identifier=sender)
        # [Visa Protocol]
        visa = msg.visa
        if visa is not None:
            facebook.save_document(document=visa)
        # check message delegate
        if msg.delegate is None:
            msg.delegate = self.messenger
        #
        # TODO: check [Meta Protocol]
        #       make sure the sender's meta exists
        #       (do in by application)
        #
        assert msg.signature is not None, 'message signature cannot be empty: %s' % msg
        # verify 'data' with 'signature'
        return msg.verify()

    def decrypt_message(self, msg: SecureMessage) -> Optional[InstantMessage]:
        # TODO: make sure private key (decrypt key) exists before decrypting message
        facebook = self.facebook
        receiver = msg.receiver
        user = facebook.select_user(receiver=receiver)
        if user is None:
            # current users not match
            trimmed = None
        elif receiver.is_group:
            # trim group message
            trimmed = msg.trim(member=user.identifier)
        else:
            trimmed = msg
        if trimmed is None:
            # not for you?
            raise LookupError('receiver error: %s' % msg)
        # check message delegate
        if msg.delegate is None:
            msg.delegate = self.messenger
        #
        # NOTICE: make sure the receiver is YOU!
        #         which means the receiver's private key exists;
        #         if the receiver is a group ID, split it first
        #
        assert msg.data is not None, 'message data cannot be empty: %s' % msg
        # decrypt 'data' to 'content'
        return msg.decrypt()
        # TODO: check top-secret message
        #       (do it by application)
