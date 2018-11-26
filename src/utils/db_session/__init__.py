#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from flask_sqlalchemy import SQLAlchemy

db_session_options = dict(autocommit=False, autoflush=False, expire_on_commit=False)
db = SQLAlchemy(session_options=db_session_options)


def init_app(app):
    if not app:
        raise RuntimeError('app is None')

    db.init_app(app)


class DBSessionForRead(object):

    def __enter__(self):
        self.session = db.create_scoped_session(options=db_session_options)
        # self.session = db.session
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        # db.session.expunge_all()
        self.session.close()


class DBSessionForWrite(object):

    def __enter__(self):
        self.session = db.create_scoped_session(options=db_session_options)
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.session.rollback()
        else:
            self.session.commit()

        # db.session.expunge_all()
        self.session.close()


class DBSessions(object):

    _session = None
    _sessions = {}

    def get(self, tag=None):
        if tag is None:
            if self._session is None:
                return self.open()
            else:
                return self._session
        else:
            if tag not in self._sessions:
                return self.open(tag)
            else:
                return self._sessions[tag]

    def open(self, tag=None):
        if (tag is None and self._session is not None) \
                or (tag is not None and tag in self._sessions):
            raise RuntimeError('db_session [%s] already opened' % tag)

        if tag is None:
            self._session = db.session
            return self._session
        else:
            self._sessions[tag] = db.create_scoped_session(options=db_session_options)
            return self._sessions[tag]

    def close(self, tag=None):
        if (tag is None and self._session is None) \
                or (tag is not None and tag not in self._sessions):
            raise RuntimeError('db_session [%s] not exist' % tag)

        if tag is None:
            self._session.close()
            self._session = None
        else:
            self._sessions[tag].close()
            self._sessions.pop(tag)

    def commit(self, tag=None):
        if (tag is None and self._session is None) \
                or (tag is not None and tag not in self._sessions):
            raise RuntimeError('db_session [%s] not exist' % tag)

        if tag is None:
            self._session.commit()
        else:
            self._sessions[tag].commit()

    def rollback(self, tag=None):
        if (tag is None and self._session is None) \
                or (tag is not None and tag not in self._sessions):
            raise RuntimeError('db_session [%s] not exist' % tag)

        if tag is None:
            self._session.rollback()
        else:
            self._sessions[tag].rollback()

    def close_all(self):
        if self._session is not None:
            self.close()

        for k in self._sessions:
            self._sessions[k].close()

        self._sessions.clear()

    def commit_all(self):
        if self._session is not None:
            self.commit()

        for k in self._sessions:
            self.commit(k)

    def rollback_all(self):
        if self._session is not None:
            self.rollback()

        for k in self._sessions:
            self.rollback(k)
