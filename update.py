import os
import re
import time
from datetime import datetime, timedelta

import feedparser
import func_timeout
import requests
from dotenv import load_dotenv
from func_timeout import func_set_timeout
from jinja2 import Environment, FileSystemLoader
from tqdm import tqdm

dotenv_path = os.path.join('.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

PER = int(os.getenv("PER"))
URL = os.getenv("URL")
STANDARD_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S+08:00'


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
        if 'content' in single_post.keys():
            item['description'] = single_post.content[0].value
        elif 'summary' in single_post.keys():
            item['description'] = single_post.summary
        else:
            item['description'] = single_post.title
        item['link'] = single_post.link
        item['pubDate'] = time.strftime(STANDARD_TIME_FORMAT,
                                        single_post.updated_parsed)

        items.append(item)

    return items


def time_limit_parse(author, rss_url):
    try:
        items = parse_rss(author, rss_url)
        return items
    except func_timeout.exceptions.FunctionTimedOut as e:
        print(e)
        return None


rss_list = get_rss_list()

items = []
for author, rss_url in tqdm(rss_list):
    item = time_limit_parse(author, rss_url)
    if item is not None:
        items += item
items.sort(key=lambda item: item['pubDate'], reverse=True)

update = datetime.utcnow()
update = update.strftime(STANDARD_TIME_FORMAT)

env = Environment(loader=FileSystemLoader('./templates'))
template = env.get_template('rss.j2')
content = template.render(update=update, items=items)
with open('rss.xml', 'w') as f:
    f.write(content)
