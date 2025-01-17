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
    Station & Service Provider (SP)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Station : DIM network server node
    SP      : DIM network service provider
"""

from typing import Optional, List

from dimp import EntityType, ID, Meta, Document, Visa
from dimp import ANYWHERE, EVERYWHERE
from dimp import User, UserDataSource
from dimp import BaseUser, BaseGroup


class Station(User):

    ANY = ID.create(name='station', address=ANYWHERE)
    EVERY = ID.create(name='stations', address=EVERYWHERE)

    def __init__(self, identifier: Optional[ID] = None,
                 host: Optional[str] = None, port: Optional[int] = 0):
        super().__init__()
        if identifier is None:
            identifier = self.ANY
        else:
            assert identifier.type == EntityType.STATION, 'Station ID type error: %s' % identifier
        self.__user = BaseUser(identifier=identifier)
        self.__host = host
        self.__port = port

    def __eq__(self, other) -> bool:
        if self is other:
            return True
        elif isinstance(other, ID):
            return self.identifier == other
        elif isinstance(other, User):
            return self.identifier == other.identifier

    def __str__(self) -> str:
        clazz = self.__class__.__name__
        identifier = self.identifier
        network = identifier.address.type
        host = self.host
        port = self.port
        return '<%s: %s(%d) host="%s" port=%d />' % (clazz, identifier, network, host, port)

    #
    #   Entity
    #

    @property  # Override
    def identifier(self) -> ID:
        return self.__user.identifier

    @identifier.setter
    def identifier(self, sid: ID):
        delegate = self.data_source
        user = BaseUser(identifier=sid)
        user.data_source = delegate
        self.__user = user

    @property  # Override
    def type(self) -> int:
        return self.__user.type

    @property  # Override
    def data_source(self) -> Optional[UserDataSource]:
        return self.__user.data_source

    @data_source.setter  # Override
    def data_source(self, delegate: UserDataSource):
        self.__user.data_source = delegate

    @property  # Override
    def meta(self) -> Meta:
        return self.__user.meta

    # Override
    def document(self, doc_type: Optional[str] = '*') -> Optional[Document]:
        return self.__user.document(doc_type=doc_type)

    #
    #   User
    #

    @property  # Override
    def visa(self) -> Optional[Visa]:
        return self.__user.visa

    @property  # Override
    def contacts(self) -> List[ID]:
        return self.__user.contacts

    # Override
    def verify(self, data: bytes, signature: bytes) -> bool:
        return self.__user.verify(data=data, signature=signature)

    # Override
    def encrypt(self, data: bytes) -> bytes:
        return self.__user.encrypt(data=data)

    # Override
    def sign(self, data: bytes) -> bytes:
        return self.__user.sign(data=data)

    # Override
    def decrypt(self, data: bytes) -> Optional[bytes]:
        return self.__user.decrypt(data=data)

    # Override
    def sign_visa(self, visa: Visa) -> Visa:
        return self.__user.sign_visa(visa=visa)

    # Override
    def verify_visa(self, visa: Visa) -> bool:
        return self.__user.verify_visa(visa=visa)

    #
    #   Server
    #

    @property
    def host(self) -> str:
        if self.__host is None:
            doc = self.document(doc_type='*')
            if doc is not None:
                value = doc.get_property('host')
                if value is not None:
                    self.__host = str(value)
            if self.__host is None:
                self.__host = '0.0.0.0'
        return self.__host

    @property
    def port(self) -> int:
        if self.__port == 0:
            doc = self.document(doc_type='*')
            if doc is not None:
                value = doc.get_property('port')
                if value is not None:
                    self.__port = int(value)
            if self.__port == 0:
                self.__port = 9394
        return self.__port


class ServiceProvider(BaseGroup):

    def __init__(self, identifier: ID):
        super().__init__(identifier=identifier)
        assert identifier.type == EntityType.ISP, 'Service Provider ID type error: %s' % identifier

    @property
    def stations(self):
        return self.members
