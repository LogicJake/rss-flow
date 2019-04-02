# -*- coding: utf-8 -*-
# @Author: LogicJake
# @Date:   2019-02-15 19:33:23
# @Last Modified time: 2019-04-02 15:25:00
from flask import Flask
from app.config import config
from app.blueprints.main import bp as main_bp


def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    app.register_blueprint(main_bp)
    app.after_request(after_request)
    return app
