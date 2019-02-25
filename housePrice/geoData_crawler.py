from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re
import sys
# from read_csv import csvReader
import csv
import tqdm
import multiprocessing

def read_addresses():
    """
    :return:楼盘地址式信息的列表,楼盘名称式信息的列表
    """
    # 读取csv文件中的行，每一个行的信息存为一个字典，返回一个字典类型的列表
    # csv = csvReader()
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
    address_list = []
    name_list = []
    for row in rows:
        if len(row['address'])!=0:
            if("[" in row['address']):
                row["address"] = row["address"].lstrip("[")
            if("]" in row['address']):
                row["address"] = row["address"].rstrip("]")
            address_list.append("成都市"+ row['address']+ row['name'])
            name_list.append("成都市"+ row['name'])
    # print('The address list is ', address_list)
    # print('The name list is ', name_list)
    print(list(zip(address_list,name_list))[0])
    return address_list, name_list

def write_line(datas):
    """将经纬度写入文件中"""
    if len(datas) == 0:
        print('len(datas) == 0')
        sys.exit(-1)
    with open('lon_lat.txt', 'a') as f:
        line = str(datas[0]) + ',' + str(datas[1]) + '\n'
        f.write(line)
    with open('hhhh.txt', 'a') as f:
        line = a + '\t' + str(datas[0]) + '\t' + str(datas[1]) + '\n'
        f.write(line)

def find_geo_data(address,driver):
    """
    selenium模拟点击网页，找寻经纬度
    :return[经度，维度]  float类型的列表
    """
    # 找到输入框
    input_tab = driver.find_element_by_xpath('//*[@id="localvalue"]')
    # 去掉(....)这种无用信息
    address=re.sub('[\（|\(][^(\）|\))]*[\）|\)]','',address)
    # 输入地址
    input_tab.send_keys(address)
    # 找到搜索键
    search_tab = driver.find_element_by_xpath('//*[@id="localsearch"]')
    # 点击搜索
    search_tab.click()
    # 睡1.5秒等待加载
    time.sleep(1.5)

    try:
        # 找到列表中的第一个
        first_tab = driver.find_element_by_xpath('//*[@id="no_0"]/a')
        # 点击
        first_tab.click()
        # 获得点击后的经纬度
        geo_string = driver.find_element_by_xpath('//*[@id="pointInput"]').get_attribute('data-clipboard-text')
        pattern = re.compile('\d+.\d+')
        data_strings = pattern.findall(geo_string)
        datas = []
        for string in data_strings:
            datas.append(float(string))
        print("成功找到{}的经纬度！".format(address))
        return datas
    except:
        # 找寻失败，返回异常
        raise Exception

if __name__=='__main__':
    """main 函数"""
    # 清空txt文件
    with open('lon_lat.txt','w') as f1:
        f1.write('')
    with open('hhhh.txt','w') as f2:
        f2.write('')

    addresses, names = read_addresses()
    if len(addresses) != len(names):
        print('len(addresses)!=len(names)')
        sys.exit(-1)

    url="http://api.map.baidu.com/lbsapi/getpoint/index.html?qq-pf-to=pcqq.c2c"
    # 设置chrome选项
    chrome_options = Options()
    # chrome_options.add_argument('--headless')# 运行时关闭窗口
    # 使用同一目录下的chromedriver.exe进行模拟
    driver = webdriver.Chrome('/Applications/Google Chrome.app/chromedriver',  chrome_options=chrome_options)
    # 请求网页
    driver.get(url)

    count = 0
    for a in tqdm.tqdm(addresses):
        driver.refresh()
        # if count<220:
        #     count+=1
        #     continue
        try:
            try:
                # 尝试使用“成都市+地址+楼盘名称”寻找经纬度
                datas = find_geo_data(a,driver)
                write_line(datas)
            except:
                # 尝试使用“成都市+楼盘名称”寻找经纬度
                driver.refresh()
                print('尝试使用楼盘名称查找——')
                datas = find_geo_data(names[count],driver)
                write_line(datas)
        except:
            # 两种尝试均失败，填0,0
            datas = [0,0]
            write_line(datas)

        count+=1
    # 关闭模拟浏览器
    driver.quit()
