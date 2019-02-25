# -*- coding: utf-8 -*-

from scrapy import Spider
from housePrice.items import LianjiaItem,CdfgjItem
from scrapy import Request
from scrapy.selector import Selector
import re
import sys
import tqdm

class LianjiaSpider(Spider):
    name = 'lianjia' 
    # 请求头部
    headers = {
        'User-Agent':
        'Mozilla/5.0 '
        '(Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    # 开始请求
    def start_requests(self):

        # url="https://cd.fang.lianjia.com/loupan/rs%E4%BA%9A%E7%89%B9%E5%85%B0%E8%92%82%E6%96%AF%E9%BB%84%E9%87%91%E6%97%B6%E4%BB%A3/"
        # yield Request(url,headers=self.headers,encoding='utf-8')

        count=1
        urls=[]
        while count<115:# 得到所有要请求的URL
            urls.append("https://cd.fang.lianjia.com/loupan/pg%s/"%str(count))
            count+=1
        for url in urls:
            yield Request(url, headers=self.headers,encoding='utf-8')# 生成请求，中间件收到响应会下载相应网页，返回给parse函数处理

    def process_area(self,floorArea_list):# 处理建筑面积的单位
        count = 0
        span_pattern=re.compile('<\w+>(.*?)<\/\w+>') 
        for area in floorArea_list:
            m=span_pattern.match(area)
            area=floorArea_list[count]=m.group(1)

            if len(area)==0:# 如果链家未给出建面
                floorArea_list[count]='unknown'
            elif '~' in area or '-' in area:# 如果建面的形式是xxx-xxx，计算均值
                pattern = re.compile(r'[\u4e00-\u9fff]+\s*(\d+).*?(\d+).*')
                m = pattern.match(area)
                floorArea_list[count]=str(round((int(m.group(1))+int(m.group(2)))/2))
            else: #如果不用算均值
                pattern = re.compile(r'[\u4e00-\u9fff]+\s*(\d+).*')
                m = pattern.match(area)
                floorArea_list[count]=m.group(1)
            count += 1

    def parse(self, response):
        sel = Selector(response)

        if int(sel.xpath('//div[@class="resblock-have-find"]/span[@class="value"]/text()').extract()[0])==0:
            print('此页没有楼盘')
            return 233

        #楼盘名称
        name_list=sel.xpath('//div[@class="resblock-desc-wrapper"]/div[@class="resblock-name"]/a[@class="name "]/text()').extract()#[count],start=0
        #地区&地标
        pre_address_list=sel.xpath('//div[@class="resblock-location"]/span/text()').extract()

        #地址
        address_list=sel.xpath('//div[@class="resblock-location"]/a[@href]/text()').extract()
        # with open("response.txt","w") as f:
        #     f.write(sel.response.text)
        # print(address_list)
        if len(name_list)!=len(address_list):
            print('ERR: len(name_list)!=len(address_list)')
            sys.exit()

        #建面  response.xpath('//div[@class="resblock-desc-wrapper"]/div[@class="resblock-area"]')

        floorArea_list=sel.xpath('//div[@class="resblock-area"]/span').extract()

        if len(address_list)!=len(floorArea_list):
            print('ERR len(address_list):  %s'%len(address_list))
            print('!=')
            print('len(floorArea_list)::%s'%len(floorArea_list))
            sys.exit()
        #处理建面
        self.process_area(floorArea_list)

        #房价提取，数字+单位
        prices_node=sel.xpath('//div[@class="resblock-price"]/div[@class="main-price"]')
        num_list=[]
        unit_list=[]
        count=0
        for price_node in prices_node:
            num_list.append(price_node.xpath('span[@class="number"]/text()').extract()[0])
            if num_list[count]=='价格待定':
                num_list[count]='unknown'
                unit_list.append('unknown')
            else:
                unit_list.append(price_node.xpath('span[@class="desc"]/text()').extract()[0])
            count+=1

        if len(floorArea_list)!=len(num_list) or len(num_list)!=len(unit_list):
            print('ERR: len(floorArea_list)!=len(num_list) or len(num_list)!=len(unit_list)')
            sys.exit()
        price_pattern = re.compile('.*?([\u4e00-\u9fff])\/([\u4e00-\u9fff]).*?')

        #处理单位，并由此修改价格
        count=0
        for unit in unit_list:
            if unit=='unknown'or num_list[count]=='unknown':
                count += 1
                continue
            m=price_pattern.match(unit.replace('\xa0',''))
            #a/b
            a=m.group(1)
            b=m.group(2)
            if a=='万' and b=='套':
                if num_list[count]!='unknown' and floorArea_list[count]!='unknown':
                    num_list[count]=str(round(int(num_list[count])*10000/int(floorArea_list[count])))
                else:
                    num_list[count]='unknown'
            elif a!='元' or b!='平':
                print('Error in processing the unit, not 元/平 or 万/套，a/b is %s/%s')%(a,b)
                sys.exit()
            count+=1

        # 在item的各个Field中放入信息
        i=0
        while i<len(name_list):
            if num_list[i] != 'unknown':
                item = LianjiaItem()

                item['name']=name_list[i]
                item['price']=num_list[i]
                item['address']=address_list[i]
                item['district']=pre_address_list[2*i]
                item['landmark']=pre_address_list[2*i+1]
                item['floorArea']=floorArea_list[i]
                yield item

            i+=1


class CdfgjSpider(Spider):
    name = 'cdfgj' 
    # 请求头部
    headers = {
        'User-Agent':
        'Mozilla/5.0 '
        '(Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    # 开始请求
    def start_requests(self):

        # yield Request(url,headers=self.headers,encoding='utf-8')
        # url = "http://esf.cdfgj.gov.cn/search;jsessionid=NKKUUMzTsZMLAGey0--usTN2.undefined?page=1&fb=0"
        count=1
        urls=[]
        while count<6231:# 得到所有要请求的URL
            urls.append("http://esf.cdfgj.gov.cn/search;jsessionid=NKKUUMzTsZMLAGey0--usTN2.undefined?page=%s&fb=0"%str(count))
            count+=1

        for url in tqdm.tqdm(urls):
            yield Request(url, headers=self.headers,encoding='utf-8')# 生成请求，中间件收到响应会下载相应网页，返回给parse函数处理


    def parse(self, response):
        sel = Selector(response)
        response_text = sel.extract()
        # with open("cdfgj.txt","w") as f:
        #     f.write(response_text)
        if(len(sel.xpath('//div[@class="pan-con"]').extract()) == 0):
            print('此页没有楼盘')
            return 233

        # 楼盘title
        title_list = sel.xpath('//div[@class="pan-item clearfix"]/h2/a/text()').extract()
        # print(title_list)
        # 楼盘卖方性质（个人or中介）
        isIntermediary_list = sel.xpath('//div[@class="pan-item clearfix"]/a[@class="img"]/span/text()').extract()
        # print(isIntermediary_list)
        # 面积
        floor_area_list = sel.xpath('//div[@class="pan-item clearfix"]/p[@class="p_hx"]/em/text()').extract()[::4]
        # print(floor_area_list)

        # house type户型
        house_type_list = sel.xpath('//div[@class="pan-item clearfix"]/p[@class="p_hx"]/em/text()').extract()[1::4]
        # print(house_type_list)

        # height_list 高度
        height_list = sel.xpath('//div[@class="pan-item clearfix"]/p[@class="p_hx"]/em/text()').extract()[2::4]
        # print(height_list)

        # year_built 建筑年份
        year_built_list = sel.xpath('//div[@class="pan-item clearfix"]/p[@class="p_hx"]/em/text()').extract()[3::4]
        # print(year_built_list) 
              
        # 楼盘名称
        name_list=sel.xpath('//div[@class="pan-item clearfix"]/p/text()').extract()#[count],start=0
        name_list_new = []

        # 楼盘位置
        address_list = []
        for name in name_list:
            # print(name)   
            if(name.strip() != ""):
                name_list_new.append(name.strip().split(" ")[0])
                address_list.append(name.strip().split(" ")[1])
            # print(1)  
        name_list = name_list_new

        # print(name_list)
        # print(address_list)

        # 更新单位，更新时间
        house_from_list = sel.xpath('//div[@class="pan-item clearfix"]/p[@class="p_gx"]/em/text()').extract()[::3]
        house_update_time_list = sel.xpath('//div[@class="pan-item clearfix"]/p[@class="p_gx"]/em/text()').extract()[2::3]
        # print("house_from_list")
        house_from_list = sel.xpath('//div[@class="pan-item clearfix"]/p[@class="p_gx"]/em').extract()[::3]
        house_update_time_list = sel.xpath('//div[@class="pan-item clearfix"]/p[@class="p_gx"]/em').extract()[2::3]

        new_house_from_list = []
        for house_from in house_from_list:
            new_house_from_list.append(Selector(text=house_from).xpath("//text()").extract()[0])
        new_house_update_time_list = []
        for house_update_time in house_update_time_list:
            new_house_update_time_list.append(Selector(text=house_update_time).xpath("//text()").extract()[0])
        house_from_list = new_house_from_list
        house_update_time_list = new_house_update_time_list

        # print(house_from_list)
        # print(house_update_time_list)

        # print(Selector(text=house_from_list[0]).xpath("//text()").extract()[0])
        # h_price 单价
        house_h_price_list = sel.xpath('//div[@class="pan-item clearfix"]/strong[@class="h-price"]/text()').extract()
        # print(house_h_price_list)

        # total_price 总价格
        house_total_price_list = sel.xpath('//div[@class="pan-item clearfix"]/strong[@class="total-price"]/i/text()').extract()
        # print(house_total_price_list)

        # 房屋信息是否已经进过核验
        house_trust_list = sel.xpath('//div[@class="pan-item clearfix"]/strong[@class="heyan"]/div[@class="yhy"]/text()').extract()
        # print(house_trust_list)

        # 房屋核验id
        house_id_list = sel.xpath('//div[@class="pan-item clearfix"]/strong[@class="heyan"]/div[@class="ynum"]/a/text()').extract()
        # print(house_id_list)

        # 房屋是否可以售卖
        house_canSale_status_list = sel.xpath('//div[@class="pan-item clearfix"]/strong[@class="status-four"]/em[@class=" yellow"]/text()').extract()
        # print(house_canSale_status_list)

        # 房屋是否有抵押
        house_mortgage_status_list = sel.xpath('//div[@class="pan-item clearfix"]/strong[@class="status-four"]/em[@class="right-5 green"]/text()').extract()
        # print(house_mortgage_status_list)

        i=0
        while i<len(name_list):
            item = CdfgjItem()
            item['house_id'] = house_id_list[i]
            item['name'] = name_list[i]
            item['address'] = address_list[i]
            item['floor_area'] = floor_area_list[i]
            item['house_type'] = house_type_list[i]
            item['height'] = height_list[i]
            item['year_built'] = year_built_list[i]
            item['house_update_time'] = house_update_time_list[i]
            item['house_from'] = house_from_list[i]
            item['house_h_price'] = house_h_price_list[i]
            item['house_total_price'] = house_total_price_list[i]
            item['house_trust'] = house_trust_list[i]
            item['house_canSale_status'] = house_canSale_status_list[i]
            item['house_mortgage_status'] = house_mortgage_status_list[i]

            yield item

            i+=1




