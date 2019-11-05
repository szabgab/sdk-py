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
    Query Group Command Processor
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    1. query for group members-list
    2. any existed member or assistant can query group members-list
"""

from dimp import ID
from dimp import InstantMessage
from dimp import Content
from dimp import GroupCommand, QueryCommand

from .group import GroupCommandProcessor


class QueryCommandProcessor(GroupCommandProcessor):

    def __response(self, group: ID, receiver: ID) -> Content:
        members = self.facebook.members(identifier=group)
        if members is None or len(members) == 0:
            raise ValueError('group members not found: %s' % group)
        return GroupCommand.reset(group=group, members=members)

    #
    #   main
    #
    def process(self, content: Content, sender: ID, msg: InstantMessage) -> Content:
        if type(self) != QueryCommandProcessor:
            raise AssertionError('override me!')
        assert isinstance(content, QueryCommand), 'group command error: %s' % content
        group: ID = self.facebook.identifier(content.group)
        # 1. check permission
        if not self.exists_member(member=sender, group=group):
            if not self.exists_assistant(member=sender, group=group):
                raise AssertionError('only member/assistant can query: %s' % msg)
        # 2. response group members for sender
        return self.__response(group=group, receiver=sender)


# register
GroupCommandProcessor.register(command=GroupCommand.QUERY, processor_class=QueryCommandProcessor)