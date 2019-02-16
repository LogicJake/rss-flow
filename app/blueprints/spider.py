# -*- coding: utf-8 -*-
# @Author: LogicJake
# @Date:   2019-02-15 20:12:43
# @Last Modified time: 2019-02-16 12:43:53
import requests
import re
import feedparser
import time
from flask import Flask
from werkzeug.contrib.cache import SimpleCache
import os
from app.config import logger
from func_timeout import func_set_timeout
import func_timeout
import multiprocessing

cache = SimpleCache()
PER = int(os.getenv("PER"))
EXPIRE = int(os.getenv("EXPIRE"))
URL = os.getenv("URL")
TITLE = os.getenv("TITLE")
ADMIN_NAME = os.getenv("ADMIN_NAME")


def get_rss_list():
    html = requests.get(URL)

    rss = re.findall('<td>(.*?)</td>', html.text)
    rss_list = []
    for i in range(len(rss)):
        if i % 3 == 0 and rss[i + 2] != '-':
            author = re.search('>(.*?)<', rss[i]).group(1)
            rss_url = rss[i + 2]
            rss_list.append([author, rss_url])
    return rss_list


@func_set_timeout(30)
def parse_rss(author, rss_url):
    feeds = feedparser.parse(rss_url)
    items = []

    for single_post in feeds.entries[:PER]:
        item = {}
        item['author'] = author
        item['title'] = single_post.title
        if single_post.has_key('content'):
            item['description'] = single_post.content[0].value
        elif single_post.has_key('summary'):
            item['description'] = single_post.summary
        else:
            item['description'] = single_post.title
        item['link'] = single_post.link
        item['pubDate'] = time.strftime(
            "%Y-%m-%d %H:%M:%S", single_post.updated_parsed)

        items.append(item)

    return items


def time_limit_parse(author, rss_url):
    try:
        items = parse_rss(author, rss_url)
        logger.info(rss_url + ' over')
        return items
    except func_timeout.exceptions.FunctionTimedOut as e:
        logger.error(rss_url)
        logger.error(e)
        return None


def generate_all():
    rss_list = get_rss_list()

    items = []
    results = []
    pool = multiprocessing.Pool(int(os.getenv('PROCESSES')))
    for author, rss_url in rss_list:
        results.append(pool.apply_async(time_limit_parse, (author, rss_url, )))

    pool.close()
    pool.join()

    for res in results:
        item = res.get()
        if item is not None:
            items += item

    items.sort(key=lambda item: item['pubDate'], reverse=True)
    return items


def ctx():
    content = cache.get('content')
    if content is None:
        logger.info('not hit cache')
        items = generate_all()
        content = {
            'items': items,
            'link': URL,
            'title': TITLE,
            'generator': ADMIN_NAME,
            'lastBuildDate': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            'ttl': EXPIRE * 60
        }
        cache.set('content', content, timeout=EXPIRE * 60)
    return content
