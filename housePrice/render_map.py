from pyecharts import Map
from read_csv import csvReader
from region_avg_price import regionAvgCalculator

def region_avgPrice_dict(csv_fpath):
    """
    利用csvReader读取csv文件中的房价信息
    利用regionAvgCalculator计算房价
    :param csv_fpath: 要读取csv文件的路径
    :return: region_avgPrice_dict
    """
    csvs=csvReader()
    cal=regionAvgCalculator()

    matrix=csvs.read_csv(csv_fpath)
    rows=csvs.extract_matrix(matrix)

    for row in rows:
        if row['district']=='' or row['price']=='':
            continue

        district = row['district']
        price = row['price']

        cal.add_price(district,price)

    return cal.calculate_avgs()

def draw_map(region_avgPrice_dict):
    attrs=[]
    values=[]
    for region,avgPrice in region_avgPrice_dict.items():
        attrs.append(region)
        values.append(avgPrice)

    map = Map("成都地图示例", width=1200, height=600)
    map.add("", attrs, values, maptype='成都', is_visualmap=True,is_roam=True,is_map_symbol_show=False,
            visual_text_color='#000')
    map.render()

if __name__=='__main__':
    draw_map(region_avgPrice_dict('lianjia.csv'))
