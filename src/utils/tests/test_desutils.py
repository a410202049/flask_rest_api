#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import base64
import binascii

from Crypto.Cipher import DES3, DES
from binascii import a2b_hex, b2a_hex

from test.unit.base import BaseTestCase
from Crypto import Random
from utils.desutils import Des3FileUtils
from utils.fileutils import FileUtils

BS = 8
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[:-ord(s[len(s)-1:])]

class Des3FileUtilsTestCase(BaseTestCase):
    """
    Des3FileUtilsTestCase
    iconv -f UTF-8 -t GB2312 IMGDOC0001_AXF_20180507_0001B.txt > IMGDOC0001_AXF_20180507_0001.txt
    """
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_padding(self):
        a = '12345678'
        b = '123'
        c = '1234567890'

        print len(pad(a))
        print len(pad(b))
        print len(pad(c))

        print ord(pad(a)[-1])
        print ord(pad(b)[-1])
        print ord(pad(c)[-1])

    def test_encrypt_file(self):
        file_path = '/Users/apple/PycharmProjects/workspace/axf_library/library/utils/tests/pic.zip'
        # file_path = '/Users/apple/PycharmProjects/workspace/axf_library/library/utils/tests/new.txt'
        with open(file_path, 'rb') as this_file:
            content = this_file.read()
        print content
        content = base64.b64encode(content)
        # content = content.replace('\n', '')

        key = '132e8a57b4f6139b3a5de9g4'

        des3 = DES3.new(key, DES3.MODE_ECB)
        content = pad(content)
        content = des3.encrypt(content)
        content = base64.encodestring(content)

        with open('./IMGDOC0001_AXF_20180514_0001.zip', 'wb') as out_file:
        # with open('./encrypt_new.txt', 'wb') as out_file:
            out_file.write(content)
        print 'ok'

    def test_decrypt_file(self):
        content = FileUtils.read_all_data(
            '/Users/apple/PycharmProjects/workspace/axf_library/library/utils/tests/J_CBIB0020_AXF_20180605.zip')
        # content = base64.decodestring(content)
        # print content
        # print b2a_hex(content)
        key = '132e8a57b4f6139b3a5de9g4'
        # Des3FileUtils.encrypt_file("/Users/apple/liaoshanqing/tmp/test_file_crypt.txt",
        #                            '/Users/apple/liaoshanqing/tmp/test_file_crypt_1.txt', 8192, key, iv)
        # Des3FileUtils.decrypt_file('./IMGDOC0001_AWX_20170724_0002.zip',
        #                            './axf_test.zip', 8192, key)
        des3 = DES3.new(key, DES3.MODE_ECB)
        with open('./1.txt', 'wb') as out_file:
            result = des3.decrypt(content)
            # print result
            # result = base64.decodestring(result)
            # print result.decode('gbk')
            # print b2a_hex(result)
            out_file.write(result)
        print 'ok'

    def test_decrypt_file1(self):
        from urllib import unquote_plus
        # content = 'MERCHANTID=123456789&POSID=000000000&BRANCHID=110000000&APPID=10301&APPNAME=测试有限公司&NUSERID=10020003000400&NAME=张三&IDTYPE=1010&USERID=440881198905280716&TXCODE=DS0000&TIMESTAMP=1526284856485'
        key = '7a46f90f1a4acc75ad1ccb4d020111'
        content = '4N%2CCFuUG2WGjYplHPM2%2CQq%2FkyWtAAs5yuhO2fcweLcfMNCAfAvRYMF4esLmCf8wS%2CLRmwWV0jF0y%0Ae21OX7K0LTJ7bU5fsrQtvtTrLs60ysSW0fLQvKqirOdXqQ6MwRYLAGeZs3QWDTMye21OX7K0LdoL%0AWo4C%2CsUl51epDozBFgs%2C0sUCZKElHNoLWo4C%2CsUlRb76z5muBMAr%2CYIk1F4v%2CnLStr9mWl8NVijR%0A%2CnoBdInIjHJiK8IQLQUdLu2C7BN82VR4uDcjkqAvdYfPSSu%2FYlATdbqEXwBsa%2CDVHjlofM9xMca2%0A1MIbLNZIdMBaHEp021UejNiPOlFLTsgmyPRy1VNqzuQLZrHz7XSbY2VImf3nlkV212zg%2FW3%2CyrE7%0ArWDnY6hjnI1jL75rpdgIUVVzRwBUcIPSk4HPdmfVR9jZ%2CKJIDYuhubHugK8VzeXtU7v37hmdNZnn%0AfBMHkNJ09UbdgLtZlTKZuCbsxXHAfFSqDXY0MvVgKqFHLM2NAROURYnA'
        # content = '10FX1h5ve9t7nX7tthXW9YW4iYTzgQhOWsQRJJN9K6zAxC8dhMBaXjOpHg5Vl3Ah'
        content = unquote_plus(content)
        content = content.replace(',', '+')
        content = base64.decodestring(content)
        des3 = DES.new(key[:8], DES3.MODE_ECB)
        result = des3.decrypt(content)
        r1 = binascii.b2a_hex(result)
        result = unpad(result)
        r2 = binascii.b2a_hex(result)
        print r1
        print r2

        print result.decode('utf-16')

    def utf16bebom(self, value):
        result = value.encode('utf-16be')
        return chr(0xfe) + chr(0xff) + result

    def test_encrypt(self):
        # content = 'MERCHANTID=123456789&POSID=000000000&BRANCHID=110000000&APPID=10301&APPNAME=测试有限公司&NUSERID=10020003000400&NAME=张三&IDTYPE=1010&USERID=440881198905280716&TXCODE=DS0000&TIMESTAMP=1526284856485'
        content = 'MERCHANTID'
        # content = content.encode('utf-16be')
        # s = binascii.b2a_hex(content)
        # print s
        content = self.utf16bebom(content)

        # # content = u'MERCHANTID=123456789'
        key = '7a46f90f1a4acc75ad1ccb4d020111'
        from urllib import quote, quote_plus

        des3 = DES.new(key[:8], DES.MODE_ECB)
        r1 = binascii.b2a_hex(content)
        content = pad(content)
        # r2 = binascii.b2a_hex(content)
        print r1
        # print r2
        content = des3.encrypt(content)
        content = base64.encodestring(content)
        content = content.strip()
        print 1
        print content
        content = content.replace('+', ',')
        print content
        content = quote_plus(content)
        print content


