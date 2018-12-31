## 如何使用爬虫部分
- 运行MovieWeb/src/movie/maoyan/spider_port.py即可更新数据库  
- 其中的run_spider函数通过传入更新的年份列表、数据库的路径，进行选择性地更新数据库  
  1. 其中年份对应如下：10：2015, 11：2016, 12:2017, 13:2018  
  2. 数据库存储在MovieWeb/src/movie/maoyan/db.sqlite下更新它只需要在run_spider函数中数据库路径传入‘db.sqlite’即可  

## 爬虫的一点介绍
- 爬取对象是 https://maoyan.com/films?showType=3&sortId=3 这个子网页，每年的爬取深度是16页
- 爬取框架使用了scrapy，并在下载中间件集成了selenium框架用于模仿浏览器请求
- 最后与sqlite数据库对接
