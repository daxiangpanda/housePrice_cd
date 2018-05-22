# housePrice
使用scrapy和pyecharts制作成都房价地图

scrapy爬虫：爬取成都链家的楼盘信息

1. 使用方法：在terminal下，进入scrapy.cfg所在的根目录，输入"scrapy crawl lianjia"开始爬取
     如果需要将爬取结构生成csv文件，则输入"scrapy crawl lianjia -o lianjia.csv"；运行之后会在根目录生成lianjia.csv文件，可用Excel打开查看（如为乱      码可自行调整Excel编码为utf-8）。
     
2. 参考文档：http://scrapy-chs.readthedocs.io/zh_CN/1.0/intro/tutorial.html

read_csv.py：读取爬虫生成的csv文件

pyecharts地图程序：生成简易的成都楼盘均价地图

1. 使用方法：运行render_map.py；运行之后会在根目录生成render.html文件。打开html文件即可查看绘制结果。
  
2. 参考文档：http://pyecharts.org/#/

