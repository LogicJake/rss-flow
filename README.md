## 流程：
- 从 https://blogroll.a2os.club 获取所有rss地址
- 遍历解析每一条rss，取每个rss的第一个item
- 对所有item根据pubDate排序，扔进rss模块

## 应用配置
修改 .env 文件

* PER:每个人的rss取多少条item
* URL:博客地址

## 运行
开启仓库 GitHub Pages 功能，github action 每隔一段时间抓取更新 rss.xml 文件。

## 其他
采用多进程解析rss，但由于feedparser的原因，解析rss的时候可能会卡住，所以设置了每条rss解析的超时时间（30s），防止整个rss的生成卡住。  