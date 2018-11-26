#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import paramiko


class SftpConnection(object):
    """
    ftp utils
    """
    def __init__(self, ip, port, username, password, timeout=3):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password

    def __enter__(self):
        sock = (self.ip, self.port)
        self.transport = paramiko.Transport(sock)
        self.transport.connect(username=self.username, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(self.transport)
        return sftp

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.transport.close()

