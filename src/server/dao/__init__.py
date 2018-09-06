#!/usr/bin/python
# -*- encoding: utf-8 -*-


class BaseConfig(object):
    @classmethod
    def from_map(cls, mapping):
        prefix = getattr(cls, '__prefix__', '').upper()

        for k in cls.__dict__:
            if not 'k'.startswith('_') and k.isupper():
                k = prefix + k
                if k in mapping:
                    setattr(cls, k, mapping[k])

    @classmethod
    def from_obj(cls, obj):
        cls.from_map(obj.__dict__)


_sql_session_options = dict(autocommit=False, autoflush=False, expire_on_commit=False)
_sql_db = None


class Config(BaseConfig):
    MAX_PAY_PASSWORD_FAIL_COUNT = 3
    LOCK_PAY_PASSWORD_SECONDS = 60 * 60 * 3


def init_app(app):
    if not app:
        return

    Config.from_map(app.config)

    global _sql_db

    from flask_sqlalchemy import SQLAlchemy
    _sql_db = SQLAlchemy(app=app, session_options=_sql_session_options)


def get_sql_session():
    return _sql_db.session


class DBSession(object):

    def __init__(self):
        super(DBSession, self).__init__()

        self._sql_session = None

    def get_sql_session(self):
        if not self._sql_session:
            self._sql_session = get_sql_session()

        return self._sql_session

    def commit(self):
        if self._sql_session:
            self._sql_session.commit()

    def rollback(self):
        if self._sql_session:
            self._sql_session.rollback()

    def close(self):
        if self._sql_session:
            self._sql_session.close()

    def flush(self):
        if self._sql_session:
            self._sql_session.flush()


class BaseDao(object):
    def __init__(self, context=None, commit_after_finish=False, dao=None):
        """
        create a dao by context and commit_after_finish or another dao
        :param context: context
        :param commit_after_finish: True / False
        :param dao: another dao
        """
        if dao:
            self._db_session = dao._db_session

            self.context = dao.context
            self.commit_after_finish = dao.commit_after_finish
            self.log = dao.log
        else:
            self._db_session = DBSession()

            self.context = context
            self.commit_after_finish = commit_after_finish

    def __enter__(self):
        return self

    def get_sql_session(self):
        return self._db_session.get_sql_session()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.commit_after_finish and exc_type:
            self._db_session.rollback()
        else:
            self._db_session.commit()

        self._db_session.close()

    def flush(self):
        self._db_session.flush()


def dao_method(func):
    def wrapper(self, *args, **kwargs):
        dao_name = self.__class__.__name__
        func_name = func.__name__


        return func(self, *args, **kwargs)

    return wrapper


class Err(object):
    DUPLICATE_NAME_CONFIG = -1
    NO_ECARD_VERIFY_TYPE = -1
