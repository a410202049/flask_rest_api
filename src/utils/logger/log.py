#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import logging
import logging.config


def get_logger(context=None, name=None):
    """
    获取日志
    :param name:
    :param context:
    :return:
    """
    logger = logging.getLogger(name if name else 'root')

    context = context if context else object
    base_extra = dict(
        request_id=context.__dict__.get('request_id', None),
        request_timestamp=context.__dict__.get('request_timestamp', None),
        ip=context.__dict__.get('ip', 'unknown'),
        hostname=context.__dict__.get('hostname', 'unknown'),
        server_name=context.__dict__.get('server_name', 'unknown'),
        server_version=context.__dict__.get('server_version', 'unknown'),
        api_version=context.__dict__.get('api_version', 'v2.0'),
        config_name=context.__dict__.get('config_name', 'unknown'),
        method=context.__dict__.get('method', 'unknown'),
        log_type=context.__dict__.get('log_type', 'unknown'),
        path=context.__dict__.get('path', 'unknown'),
    )

    normal_extra = dict(
        service_name=context.__dict__.get('service_name', 'unknown'),
        service_version=context.__dict__.get('service_version', 'unknown'),
    )

    context_property = context.__dict__.items()
    for key, value in context_property:
        if key.startswith('extra_'):
            base_extra.update({key: value})
    base_extra.update(normal_extra)
    logger = logging.LoggerAdapter(logger, base_extra)

    return logger


def init_logger_from_file(config):
    """
    初始化日志, file
    :param config:
    :return:
    """
    logging.config.fileConfig(config)


def init_logger_from_object(config):
    """
    初始化日志, dict
    :param config:
    :return:
    """
    level = config.DEBUG if hasattr(config, 'DEBUG') and config.DEBUG else 'INFO'
    log_path = config.LOG_PATH if hasattr(config, 'LOG_PATH') else 'demo.log'
    network_formatter_default = '[%(levelname)1.1s][%(method)s][tm:%(asctime)s][request_id:%(request_id)s]' \
                                '[request_timestamp:%(request_timestamp)s][service:%(service_name)s]' \
                                '[service_version:%(service_version)s][api_version:%(api_version)s]' \
                                '[pt:%(process)d:%(thread)d][file:%(module)s:%(funcName)s:%(lineno)d] %(message)s'
    network_formatter = config.NETWORK_FORMATTER if hasattr(config, 'NETWORK_FORMATTER') else network_formatter_default

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'root_formatter': {
                'format': '[%(levelname)1.1s][tm:%(asctime)s][pt:%(process)d:%(thread)d]'
                          '[file:%(module)s:%(funcName)s:%(lineno)d][%(pathname)s] %(message)s',
                'datefmt': "%Y-%m-%d %H:%M:%S",
            },
            'network_formatter': {
                'format': network_formatter,
                'datefmt': "%Y-%m-%d %H:%M:%S",
            },
        },
        'handlers': {
            # 'root_file': {
            #     'level': level,
            #     'class': 'library.logger.handlers.TimedRotatingFileHandler.TimedRotatingFileHandler',
            #     'filename': log_path,
            #     'when': 'midnight',
            #     'interval': 1,  # day
            #     'backupCount': 7,
            #     'formatter': 'root_formatter',
            # },
            # 'network_file': {
            #     'level': level,
            #     'class': 'library.logger.handlers.TimedRotatingFileHandler.TimedRotatingFileHandler',
            #     'filename': log_path,
            #     'when': 'midnight',
            #     'interval': 1,  # day
            #     'backupCount': 7,
            #     'formatter': 'network_formatter',
            # },
            'root_file': {
                'level': level,
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': log_path,
                'formatter': 'root_formatter',
                'maxBytes': 1024 * 1024 * 10,  # 文件大小 5M
                'backupCount': 7,  # 备份份数
                'encoding': 'utf8',  # 文件编码
            },
            'network_file': {
                'level': level,
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': log_path,
                'formatter': 'network_formatter',
                'maxBytes': 1024 * 1024 * 10,  # 文件大小 5M
                'backupCount': 7,  # 备份份数
                'encoding': 'utf8',  # 文件编码
            },
            'root_console': {
                'level': level,
                'class': 'logging.StreamHandler',
                'formatter': 'root_formatter',
            },
            'network_console': {
                'level': level,
                'class': 'logging.StreamHandler',
                'formatter': 'network_formatter',
            },
        },
        'loggers': {
            '': {
                'handlers': ['root_file', 'root_console'],
                'level': config.DEBUG if config.DEBUG else 'INFO',
            },
            '__main__': {
                'handlers': ['root_file', 'root_console'],
                'level': config.DEBUG if config.DEBUG else 'INFO',
            },
            # 'sqlalchemy': {
            #     'handlers': ['root_file', 'root_console'],
            #     'level': config.DEBUG if config.DEBUG else 'INFO',
            # },
            # 'sqlalchemy.engine': {
            #     'handlers': ['root_file', 'root_console'],
            #     'level': config.DEBUG if config.DEBUG else 'INFO',
            # },
            # 'sqlalchemy.dialects.postgresql': {
            #     'handlers': ['root_file', 'root_console'],
            #     'level': config.DEBUG if config.DEBUG else 'INFO',
            # },
            'root': {
                'handlers': ['root_file', 'root_console'],
                'level': config.DEBUG if config.DEBUG else 'INFO',
            },
            'network': {
                'handlers': ['network_file', 'network_console'],
                'level': config.DEBUG if config.DEBUG else 'INFO',
            },
        }
    }

    logging.config.dictConfig(LOGGING)
