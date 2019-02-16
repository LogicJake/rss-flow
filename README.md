## 流程：
- 从 https://blogroll.a2os.club 获取所有rss地址
- 遍历解析每一条rss，取每个rss的第一个item
- 对所有item根据pubDate排序，扔进rss模块

## 应用配置
修改 .env 文件

* FLASK_ENV:flask环境，决定项目启动时的模式
* EXPIRE:缓存过期时间
* TITLE:rss模板的title字段
* ADMIN_NAME:rss模板的generator字段
* PER:每个人的rss取多少条item
* URL:博客地址
* PROCESSES:进程数

## 安装运行
```
pip install -r requirements.txt
flask run -h 0.0.0.0
```
访问 `127.0.0.1:5000` 即可

## 其他
采用多进程解析rss，但由于feedparser的原因，解析rss的时候可能会卡住，所以设置了每条rss解析的超时时间（30s），防止整个rss的生成卡住。  
采用了简单的内存缓存，缓存过期时间为10min，缓存过期后会重新抓取生成，需一定的时间。
