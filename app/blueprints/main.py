# -*- coding: utf-8 -*-
# @Author: LogicJake
# @Date:   2019-02-15 20:04:12
# @Last Modified time: 2019-02-15 21:35:28
from flask import Blueprint, render_template, request
bp = Blueprint('main', __name__)


@bp.app_template_global()
def filter_content(ctx):
    include_title = request.args.get('include_title')
    include_description = request.args.get('include_description')
    exclude_title = request.args.get('exclude_title')
    exclude_description = request.args.get('exclude_description')
    limit = request.args.get('limit', type=int)
    items = ctx['items'].copy()
    items = [item for item in items if include_title in item[
        'title']] if include_title else items
    items = [item for item in items if include_description in item[
        'description']] if include_description else items
    items = [item for item in items if exclude_title not in item[
        'title']] if exclude_title else items
    items = [item for item in items if exclude_description not in item[
        'description']] if exclude_description else items
    items = items[:limit] if limit else items
    ctx = ctx.copy()
    ctx['items'] = items
    return ctx


@bp.route('/')
def index():
    from .spider import ctx
    return render_template('rss.xml', **filter_content(ctx())), 200, {'Content-Type': 'text/xml; charset=utf-8'}
