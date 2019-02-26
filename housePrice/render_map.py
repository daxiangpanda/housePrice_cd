from pyecharts import Map,Geo
import csv
# from read_csv import csvReader
from region_avg_price import regionAvgCalculator

def region_avgPrice_dict(csv_fpath):
    """
    利用csvReader读取csv文件中的房价信息
    利用regionAvgCalculator计算房价
    :param csv_fpath: 要读取csv文件的路径
    :return: region_avgPrice_dict
    """
    with open("housePrice_cd/hhhh.txt","r") as f:
        geo_list = f.read().split("\n")
    geo_dict = {}
    for geo in geo_list:
        geo_detail = geo.split("\t")
        if(len(geo_detail) == 3):
            if(geo_detail[1] != '0'):
                geo_name = geo_detail[0]
                geo_x = geo_detail[1]
                geo_y = geo_detail[2]
                geo_dict[geo_name] = [float(geo_x),float(geo_y)]

    # print(geo_dict)
    with open("housePrice_cd/housePrice/cdfgj.csv","r") as f:
        maxtrix = list(csv.reader(f))
    # maxtrix = csv.reader()
    item_names = maxtrix[0]
    rows = []
    for row in maxtrix[1:]:
        item_dic = {}
        for name_index in range(len(item_names)):
            item_dic[item_names[name_index]] = row[name_index]
        rows.append(item_dic)
    # rows = csv.extract_matrix(maxtrix)
    # 返回两个键入搜索框的列表
    attrs = []
    values = []
    for row in rows:
        if len(row['address'])!=0:
            if("[" in row['address']):
                row["address"] = row["address"].lstrip("[")
            if("]" in row['address']):
                row["address"] = row["address"].rstrip("]")
            # print(row["name"])
            # print(list(geo_dict.keys())[:10])
            # break
            if("成都市"+ row['address']+ row['name'] in geo_dict):
                attrs.append("成都市"+ row['address']+ row['name'])
                values.append(int(row["house_h_price"][:-3])) 
    # print(name_list)
    # csvs=csvReader()
    # cal=regionAvgCalculator()

    # matrix=csvs.read_csv(csv_fpath)
    # rows=csvs.extract_matrix(matrix)

    # for row in rows:
    #     if row['district']=='' or row['price']=='':
    #         continue

    #     district = row['district']
    #     price = row['price']

    #     cal.add_price(district,price)

    return attrs,values,geo_dict

def draw_map(region_avgPrice_dict):
    # attrs=["小区1","小区2"]
    # values=[9000,8000]
    # print(region_avgPrice_dict("").items())
    attrs,values,geo_dict = region_avgPrice_dict
    print(values)
    # for region,avgPrice in region_avgPrice_dict.items():
    #     attrs.append(region)
    #     values.append(avgPrice)
    geo = Geo("成都市二手房价热力图","",
        title_color="#fff",
        title_pos="center",
        width=1200,
        height=600,
        background_color="#404a59",
    )

    geo.add(   
         "",
         attrs,
         values,
        maptype="成都",
        # type="heatmap",
        visual_range=[0, 200],
        visual_text_color="#fff",
        symbol_size=3,
        is_visualmap=True,
        visual_split_number=6,
        geo_cities_coords = geo_dict
    )

    geo.render()
    # map = Map("成都地图示例", width=1200, height=600)
    # map.add("", attrs, values, maptype='成都', is_visualmap=True,is_roam=True,is_map_symbol_show=False,
    # 
            # visual_text_color='#000')
    # map.render()

if __name__=='__main__':
    draw_map(region_avgPrice_dict('cdfgj.csv'))
