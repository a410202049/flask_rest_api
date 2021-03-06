#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from datetime import datetime

from server.models.BaseModel import Base
from sqlalchemy import Column, Integer, String, DATETIME, Boolean
from werkzeug.security import generate_password_hash, check_password_hash


class User(Base):
    """用户"""
    __tablename__ = "t_user"
    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, index=True)
    email = Column(String(64), unique=True, index=True)
    password_hash = Column(String(128))
    register_time = Column(DATETIME, default=datetime.utcnow)
    last_time = Column(DATETIME, default=datetime.utcnow)
    status = Column(Boolean, default=True)
    confirmed = Column(Boolean, default=False)
    nickname = Column(String(64))
    create_time = Column("create_time", DATETIME, nullable=False, default=datetime.now, doc=u'创建时间')
    update_time = Column("update_time", DATETIME, nullable=False, default=datetime.now, onupdate=datetime.now,
                         doc=u'更新时间')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
