# -*- coding: utf-8 -*-
# @Author: LogicJake
# @Date:   2019-02-15 19:35:17
# @Last Modified time: 2019-02-15 23:07:34
import os
import sys
import logging
import logging.config
import json
import os


os.makedirs('log', exist_ok=True)
logging.config.fileConfig('log.conf')
logger = logging.getLogger()
logger.info('Finish loading config')


basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class BaseConfig:
    SITE_NAME = os.getenv("SITE_NAME")


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    TESTING = True


class ProductionConfig(BaseConfig):
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
