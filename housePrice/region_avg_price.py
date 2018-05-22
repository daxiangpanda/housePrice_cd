class regionAvgCalculator(object):
    district_list=['都江堰市','彭州市','崇州市','大邑县','邛崃市','蒲江县','新津县','双流区','简阳市','金堂县','青白江区',
                   '新都区','郫都区','温江区','双流区','龙泉驿区','成华区','金牛区','青羊区','武侯区','锦江区']

    region_avgPrice_dict={}

    def __init__(self):
        for dist in self.district_list: #将所有地区的均值初始化为空列表
            self.region_avgPrice_dict[dist]=[]

    def add_price(self,region_name,price):
        price=int(price)
        for dist in self.district_list:
            if region_name in dist:
                self.region_avgPrice_dict[dist].append(price)
                break

    def calculate_avgs(self):
        for dist in self.district_list:
            prices=self.region_avgPrice_dict[dist]

            if type(prices)==list and len(prices)==0:
                print('在地图中没有地区 %s'%dist)
                continue
            if type(prices)==list:
                self.region_avgPrice_dict[dist]=round(sum(prices)/len(prices))

        return self.region_avgPrice_dict
