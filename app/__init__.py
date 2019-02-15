# -*- coding: utf-8 -*-
# @Author: LogicJake
# @Date:   2019-02-15 19:33:23
# @Last Modified time: 2019-02-15 20:06:40
from flask import Flask
from app.config import config
from app.blueprints.main import bp as main_bp


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    app.register_blueprint(main_bp)
    return app
