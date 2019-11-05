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

"""
    Meta Command Processor
    ~~~~~~~~~~~~~~~~~~~~~~

"""

from dimp import ID, Meta
from dimp import Envelope, Content, TextContent, MetaCommand

from ..protocol import ReceiptCommand

from .command import CommandProcessor


class MetaCommandProcessor(CommandProcessor):

    def __query(self, identifier: ID) -> Content:
        # querying meta for ID
        self.info('search meta %s' % identifier)
        meta = self.facebook.meta(identifier=identifier)
        # response
        if meta is not None:
            return MetaCommand.response(identifier=identifier, meta=meta)
        else:
            return TextContent.new(text='Sorry, meta for %s not found.' % identifier)

    def __upload(self, identifier: ID, meta: Meta) -> Content:
        # received a meta for ID
        self.info('received meta %s' % identifier)
        if self.facebook.save_meta(identifier=identifier, meta=meta):
            self.info('meta saved %s, %s' % (identifier, meta))
            return ReceiptCommand.new(message='Meta for %s received!' % identifier)
        else:
            self.error('meta not match %s, %s' % (identifier, meta))
            return TextContent.new(text='Meta not match %s!' % identifier)

    def process(self, content: Content, envelope: Envelope) -> bool:
        if type(self) != MetaCommandProcessor:
            raise AssertionError('override me!')
        assert isinstance(content, MetaCommand)
        identifier = self.facebook.identifier(content.identifier)
        meta = content.meta
        if meta is None:
            response = self.__query(identifier=identifier)
        else:
            response = self.__upload(identifier=identifier, meta=meta)
        # response to sender
        return self.messenger.send_content(content=response, receiver=envelope.sender)