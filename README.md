# 简介
这是MovieNest，一个电影分析评价推荐系统。它是2018HITSZ软件工程本科生14组的作品。

在这里，电影制作人和普通观影者都可以找到属于自己的一番天地。


# 新增功能
1. 完成了报表打印功能，可以根据不同需求打印不同的报表。
2. 添加整理了各类文档。
3. 重新录制了demo

# 依赖环境
- 连接互联网（在unpack上调用javascript依赖包）
- Python 3.7
- Vue.js 2.5
- ElementUI 2.4
- Flask 1.0.2
- Sqlite 3
- Scrapy 1.5.1
- selenium 3.141.0
- fontTools

# 使用方式
在使用前，需要先安装依赖环境
```
pip install flask scrapy selenium fontTools
```
运行爬虫
```
cd src/spider
python maoyan/spider_port.py
```
运行网站后台
```
cd src/movienest
python run.py
```
若想使用爬虫爬取下载的新版数据库，将db.sqlite复制到instance目录下，并调用
```
flask init-db
```

# 功能说明
## 账户管理
### 基础功能
1. 注册账号
2. 登录及注销
### 附加功能
1. **安全上：**  
    1. 权限控制：游客用户登录后才能使用任意的功能  
    2. 密码密文显示  
    3. 加密存储密码  
2. **用户体验上：** 
    1. 修改密码
### 实现技术
1. 用户信息使用sqlite储存
2. UPDATE语句更新修改密码
3. HTML+CSS+JAVASCRIPT实现前端
### 实现文件
- 前端：src/movienest/templates/auth文件夹中的各html文件
- 后端：src/movienest/auth.py文件

## 数据爬虫部分
### 基础功能
1.	稳定爬取
### 附加功能
1. 更新数据库  
2. 数据库存储
### 实现技术
1. Scrapy集成Selenium模仿浏览器爬取
2. 使用CrawlerProcess向spider传入参数选择更新年份进行更新
3. 数据库使用关系型数据库存储，分别有电影表、演员表、类型表、电影-演员关系表、电影-类型关系表五张表，提高访问速度
### 实现文件
- src/spider文件夹内各种文件

## 可视化部分
### 基础功能
1. 票房占比
2. 票房变化趋势
3. 票房年变化趋势
4. top电影
5. 劳模演员
### 附加功能
1. 票房份额可以选择2015到2018年任意月份间的时间段进行展示，并可以动态交互。
2. TOP电影可以选择2015到2018年任意月份间的时间段进行展示，并可以动态交互。
3. 劳模演员可以选择2015到2018年任意月份间的时间段进行展示，并可以动态交互，自动过滤出演次数为1的演员。
4. 各功能均可使用不同图表展示。
### 实现技术
1. 电影信息使用sqlite储存
2. 使用SELECT语句进行选取
3. HTML+CSS+JAVASCRIPT实现前端
4. echarts和echarts-wordcloud实现图表显示
### 实现文件
- 前端：src/movienest/templates/auth文件夹中的各html文件
- 后端：src/movienest/movienest.py文件

## 榜单功能
1. 按时间段&类别筛选的电影榜单功能（按评分排序）
2. 图表可以与用户交互
### 实现技术
1. 电影信息使用sqlite储存
2. 使用SELECT语句进行选取
3. HTML+CSS+JAVASCRIPT实现前端
4. 使用element-ui展示表格
### 实现文件
- 前端：src/movienest/templates/文件夹下的box-office.html和rating.html文件
- 后端：src/movienest/movienest.py文件

## 搜索功能
1. 根据演员名、电影名、导演名搜索电影
2. 图表可以与用户交互
### 实现技术
1. 电影信息使用sqlite储存
2. 使用SELECT语句进行选取
3. HTML+CSS+JAVASCRIPT实现前端
4. 使用element-ui展示表格
### 实现文件
- 前端：src/movienest/templates/search.html文件
- 后端：src/movienest/movienest.py文件

## 电影数据报表功能 
### 基础功能
1. 将选择的图表打印至PDF文档中
### 附加功能
1. 可以单独保存各个图表为jpg文件
### 实现技术
1. HTML+CSS+JAVASCRIPT实现前端
2. 使用getElementsByClass获取图表
3. html2canvas+jspdf进行打印
### 实现文件
- src/movienest/templates/base.html文件


