#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from Crypto.Cipher import DES3, DES, Blowfish


class Des3FileUtils(object):
    """
    使用DES3对文件加解密
    """
    @staticmethod
    def encrypt_file(in_filename, out_filename, chunk_size, key, iv):
        des3 = DES3.new(key, DES3.MODE_CFB, iv)
        with open(in_filename, 'r') as in_file:
            with open(out_filename, 'w') as out_file:
                while True:
                    chunk = in_file.read(chunk_size)
                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        chunk += ' ' * (16 - len(chunk) % 16)
                    out_file.write(des3.encrypt(chunk))

    @staticmethod
    def decrypt_file(in_filename, out_filename, chunk_size, key, iv):
        des3 = DES3.new(key, DES3.MODE_CFB, iv)
        # des3 = DES3.new(key, DES3.MODE_ECB)

        with open(in_filename, 'rb') as in_file:
            with open(out_filename, 'wb') as out_file:
                while True:
                    chunk = in_file.read(chunk_size)
                    if len(chunk) == 0:
                        break
                    out_file.write(des3.decrypt(chunk))
