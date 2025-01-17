# -*- coding: utf-8 -*-
#
#   DIM-SDK : Decentralized Instant Messaging Software Development Kit
#
#                                Written in 2019 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2019 Albert Moky
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

from mkm.types import *
from mkm.crypto import *
from mkm import *
from dkd import *
from dimp import *

from .mkm import *
from .core import *

from .cpu import *

name = 'DIM-SDK'

__author__ = 'Albert Moky'


__all__ = [

    #
    #   Types
    #
    'Wrapper', 'Stringer', 'Mapper',
    'ConstantString',
    'Dictionary',

    #
    #   Crypto
    #
    'DataCoder', 'ObjectCoder', 'StringCoder',
    'Base64', 'Base58', 'Hex', 'JSON', 'UTF8',
    'base64_encode', 'base64_decode', 'base58_encode', 'base58_decode',
    'hex_encode', 'hex_decode',
    'json_encode', 'json_decode', 'utf8_encode', 'utf8_decode',

    'DataDigester',
    'MD5', 'SHA1', 'SHA256', 'KECCAK256', 'RIPEMD160',
    'md5', 'sha1', 'sha256', 'keccak256', 'ripemd160',

    'CryptographyKey',
    'SymmetricKey', 'EncryptKey', 'DecryptKey',
    'SymmetricKeyFactory',
    'AsymmetricKey', 'SignKey', 'VerifyKey',
    'PublicKey', 'PublicKeyFactory',
    'PrivateKey', 'PrivateKeyFactory',

    #
    #   MingKeMing
    #
    'EntityType', 'MetaType',
    'Address', 'AddressFactory',
    'ID', 'IDFactory',
    'Meta', 'MetaFactory',
    'Document', 'DocumentFactory',
    'Visa', 'Bulletin',

    # 'entity_is_user', 'entity_is_group', 'entity_is_broadcast',
    # 'meta_has_seed', 'meta_type',
    # 'document_type',

    'BaseAddressFactory', 'BroadcastAddress',
    'IdentifierFactory', 'Identifier',
    'ANYWHERE', 'EVERYWHERE', 'ANYONE', 'EVERYONE', 'FOUNDER',
    'BaseMeta',
    'BaseDocument', 'BaseVisa', 'BaseBulletin',

    # 'document_identifier',

    #
    #   DaoKeDao
    #
    'ContentType',  # 'content_type',
    'Content', 'ContentFactory',
    'Envelope', 'EnvelopeFactory',
    'Message', 'InstantMessage', 'SecureMessage', 'ReliableMessage',
    'InstantMessageFactory', 'SecureMessageFactory', 'ReliableMessageFactory',
    'InstantMessageDelegate', 'SecureMessageDelegate', 'ReliableMessageDelegate',

    'BaseContent',
    'MessageEnvelope', 'MessageEnvelopeFactory',
    'BaseMessage',
    'PlainMessage', 'PlainMessageFactory',
    'EncryptedMessage', 'EncryptedMessageFactory',
    'NetworkMessage', 'NetworkMessageFactory',

    #
    #   DIMP
    #
    'TextContent', 'ForwardContent', 'ArrayContent',
    'MoneyContent', 'TransferContent',
    'FileContent', 'ImageContent', 'AudioContent', 'VideoContent',
    'PageContent', 'CustomizedContent',
    'Command', 'CommandFactory',  # 'command_name',
    'MetaCommand', 'DocumentCommand',
    'HistoryCommand', 'GroupCommand',
    'InviteCommand', 'ExpelCommand', 'JoinCommand',
    'QuitCommand', 'QueryCommand', 'ResetCommand',

    'EntityDelegate',
    'EntityDataSource', 'UserDataSource', 'GroupDataSource',
    'Entity', 'User', 'Group',
    'BaseEntity', 'BaseUser', 'BaseGroup',

    'BaseTextContent', 'SecretContent', 'ListContent',
    'BaseMoneyContent', 'TransferMoneyContent',
    'BaseFileContent', 'ImageFileContent', 'AudioFileContent', 'VideoFileContent',
    'WebPageContent', 'AppCustomizedContent',
    'BaseCommand', 'BaseMetaCommand', 'BaseDocumentCommand',
    'BaseHistoryCommand', 'BaseGroupCommand',
    'InviteGroupCommand', 'ExpelGroupCommand', 'JoinGroupCommand',
    'QuitGroupCommand', 'QueryGroupCommand', 'ResetGroupCommand',
    # 'ContentFactoryBuilder', 'CommandFactoryBuilder',
    # 'GeneralCommandFactory', 'HistoryCommandFactory', 'GroupCommandFactory',
    # 'register_message_factories', 'register_content_factories', 'register_command_factories',
    'Barrack', 'Transceiver', 'Packer', 'Processor',

    #
    #   Extends
    #
    'ServiceProvider', 'Station', 'Bot',

    'AddressNameService', 'CipherKeyDelegate', 'TwinsHelper',
    'Facebook', 'Messenger', 'MessagePacker', 'MessageProcessor',
    'ContentProcessor', 'ContentProcessorFactory', 'ContentProcessorCreator',

    'register_core_factories',

    #
    #   CPU
    #
    'BaseContentProcessorCreator', 'GeneralContentProcessorFactory',
    'BaseContentProcessor', 'BaseCommandProcessor',
    'ForwardContentProcessor', 'ArrayContentProcessor',
    'CustomizedContentProcessor', 'CustomizedContentHandler',
    'MetaCommandProcessor', 'DocumentCommandProcessor',
    'HistoryCommandProcessor', 'GroupCommandProcessor',
    'InviteCommandProcessor', 'ExpelCommandProcessor', 'QuitCommandProcessor',
    'ResetCommandProcessor', 'QueryCommandProcessor',
]
