#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import unicode_literals, absolute_import

from logging.handlers import TimedRotatingFileHandler as _TimedRotatingFileHandler
import time
import os
from logging import LogRecord


class TimedRotatingFileHandler(_TimedRotatingFileHandler):
    """
    重写日志处理模块，处理多线程日志切片问题
    """

    def __init__(
            self,
            filename,
            when='h',
            interval=1,
            backupCount=0,
            encoding=None,
            delay=False,
            utc=False):
        super(
            TimedRotatingFileHandler,
            self).__init__(
            filename,
            when,
            interval,
            backupCount,
            encoding,
            delay,
            utc)

    def doRollover(self):
        """
        do a rollover; in this case, a date/time stamp is appended to the filename
        when the rollover happens.  However, you want the file to be named for the
        start of the interval, not the current time.  If there is a backup count,
        then we have to get a list of matching filenames, sort them and remove
        the one with the oldest suffix.
        """
        if self.stream:
            self.stream.close()
        # get the time that this sequence started at and make it a TimeTuple
        t = self.rolloverAt - self.interval
        if self.utc:
            timeTuple = time.gmtime(t)
        else:
            timeTuple = time.localtime(t)
        dfn = self.baseFilename + "." + time.strftime(self.suffix, timeTuple)
        # if os.path.exists(dfn):
        #    os.remove(dfn)
        if not os.path.exists(dfn):
            os.rename(self.baseFilename, dfn)
        if self.backupCount > 0:
            # find the oldest log file and delete it
            # s = glob.glob(self.baseFilename + ".20*")
            # if len(s) > self.backupCount:
            #    s.sort()
            #    os.remove(s[0])
            for s in self.getFilesToDelete():
                os.remove(s)
        # print "%s -> %s" % (self.baseFilename, dfn)
        self.mode = 'a'
        self.stream = self._open()
        currentTime = int(time.time())
        newRolloverAt = self.computeRollover(currentTime)
        while newRolloverAt <= currentTime:
            newRolloverAt = newRolloverAt + self.interval
        # If DST changes and midnight or weekly rollover, adjust for this.
        if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and not self.utc:
            dstNow = time.localtime(currentTime)[-1]
            dstAtRollover = time.localtime(newRolloverAt)[-1]
            if dstNow != dstAtRollover:
                if not dstNow:  # DST kicks in before next rollover, so we need to deduct an hour
                    newRolloverAt = newRolloverAt - 3600
                else:  # DST bows out before next rollover, so we need to add an hour
                    newRolloverAt = newRolloverAt + 3600
        self.rolloverAt = newRolloverAt

    def handle(self, record):
        """
        重新父类方法
        """
        if isinstance(record, LogRecord):
            record.msg = msg_fiter(record.msg)
        # return TimedRotatingFileHandler.handle(self, record)
        rv = self.filter(record)
        if rv:
            self.acquire()
            try:
                self.emit(record)
            finally:
                self.release()
        return rv


def msg_fiter(msg):
    """
    过滤换行符
    """
    if isinstance(msg, str):
        while msg.find('\n') >= 0:
            msg = msg.replace('\n', ' ')
    return msg
