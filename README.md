# housePrice
使用scrapy，selenium，echarts和pyecharts制作成都房价地图

scrapy爬虫：爬取成都链家的楼盘信息

1. 运行方法：第一种：在terminal下，进入scrapy.cfg所在的根目录，输入"scrapy crawl lianjia"开始爬取。目前我们已经在pipelines.py增加了保存json文件的功能（为了生成json格式，供js代码使用），所以直接用第一种方法即可。
     第二种：如果需要将爬取结构生成csv文件，则输入"scrapy crawl lianjia -o lianjia.csv"；运行之后会在根目录生成lianjia.csv文件，可用Excel打开查看（如为乱码可自行调整Excel编码为utf-8）。
     
2. 参考文档：http://scrapy-chs.readthedocs.io/zh_CN/1.0/intro/tutorial.html

read_csv.py：读取爬虫生成的csv文件

pyecharts地图程序：生成简易的成都楼盘均价地图

1. 使用方法：运行render_map.py；运行之后会在根目录生成render.html文件。打开html文件即可查看绘制结果。
  
2. 参考文档：http://pyecharts.org/#/

经纬度爬虫：
1. 参考网址：http://selenium-python-zh.readthedocs.io/en/latest/getting-started.html
2. 编程思想：使用selenium模拟输入、点击，通过小区地址和名称获得其经纬度

transform.c
将各项数据转换为echarts散点图能用的格式。

echarts调用百度API，显示详细房价地图（echarts_test文件夹中）
1. 参考网址：https://blog.csdn.net/qq_35488769/article/details/78799964
            http://echarts.baidu.com/blog/2016/06/13/echarts-map-tutorial.html
2. 使用方法：用chrome浏览器打开"坐标转换.html"
3. 编程思想：调用百度API画地图，调用echarts制作散点图、雷达图（数据来源ln_stat.txt：来源于经纬度爬虫生成的数据）
