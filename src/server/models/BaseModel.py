#!/usr/bin/env python
# -*- coding:utf-8 -*-
import base64

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


def copy(self):
    data_obj = self.__class__()

    for k in self.__dict__:
        if k != '_sa_instance_state':
            setattr(data_obj, k, self.__dict__[k])

    return data_obj


def to_dict(self):
    dest_dict = self.__dict__.copy()
    if '_sa_instance_state' in dest_dict:
        dest_dict.pop('_sa_instance_state')

    return dest_dict


def utf8_decode(self, value, exp_default):
    if value:
        try:
            value = base64.decodestring(value).decode('utf-8')
        except Exception:
            value = exp_default

    return value


def utf8_encode(self, value, exp_default):
    if value:
        try:
            if isinstance(value, unicode):
                value = value.encode('utf-8')

            value = base64.encodestring(value)
        except Exception:
            value = exp_default

    return value


setattr(Base, 'copy', copy)
setattr(Base, 'to_dict', to_dict)
setattr(Base, 'utf8_encode', utf8_encode)
setattr(Base, 'utf8_decode', utf8_decode)

__author__ = 'seaman'


