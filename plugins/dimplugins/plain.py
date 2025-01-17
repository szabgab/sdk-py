# -*- coding: utf-8 -*-
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

from typing import Optional

from .keys import BaseSymmetricKey


class PlainKey(BaseSymmetricKey):
    """
        Symmetric key for broadcast message,
        which will do nothing when en/decoding message data
    """
    PLAIN = 'PLAIN'

    def __init__(self, key: Optional[dict] = None):
        if key is None:
            key = {'algorithm': self.PLAIN}
        super().__init__(key=key)

    @property
    def size(self) -> int:
        return 0

    @property  # Override
    def data(self) -> bytes:
        return b''

    # Override
    def encrypt(self, data: bytes) -> bytes:
        return data

    # Override
    def decrypt(self, data: bytes) -> Optional[bytes]:
        return data
