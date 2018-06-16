from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re
import sys
from read_csv import csvReader
# [lon,lat]
# C:\Users\lenovo\PycharmProjects\housePrice-master\housePrice\read_csv.py
def read_addresses():
    """
    :return:楼盘地址的列表,楼盘名称的列表
    """
    # 读取csv文件中的行，每一个行的信息存为一个字典，返回一个字典类型的列表
    csv = csvReader()
    maxtrix = csv.read_csv(r"lianjia.csv")
    rows = csv.extract_matrix(maxtrix)
    # 返回两个键入搜索框的列表
    address_list = []
    name_list = []
    for row in rows:
        if len(row['address'])!=0:
            address_list.append("成都市"+ row['address']+ row['name'])
            name_list.append("成都市"+ row['name'])
    print('The address list is ', address_list)
    print('The name list is ', name_list)
    return address_list, name_list

def write_line(datas):
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

    input_tab = driver.find_element_by_xpath('//*[@id="localvalue"]')
    # keys="%s%s"%("成都市",address)
    address=re.sub('[\（|\(][^(\）|\))]*[\）|\)]','',address)
    # address=re.sub('\([^\)]*\)','',address)
    input_tab.send_keys(address)
    search_tab = driver.find_element_by_xpath('//*[@id="localsearch"]')
    search_tab.click()
    time.sleep(1.5)

    try:
        first_tab = driver.find_element_by_xpath('//*[@id="no_0"]/a')
        first_tab.click()
        geo_string = driver.find_element_by_xpath('//*[@id="pointInput"]').get_attribute('data-clipboard-text')
        # driver.quit()
        pattern = re.compile('\d+.\d+')
        data_strings = pattern.findall(geo_string)
        datas = []
        for string in data_strings:
            datas.append(float(string))
        print("成功"+address)
        return datas
    except:
        raise Exception
        print("失败" + address)



if __name__=='__main__':
    # 清空txt文件
    with open('lon_lat.txt','w') as f1:
        f1.write('')
    with open('hhhh.txt','w') as f2:
        f2.write('')
    addresses, names = read_addresses()
    if len(addresses) != len(names):
        print('len(addresses)!=len(names)')
        sys.exit(-1)

    # chrome模拟进行请求
    url="http://api.map.baidu.com/lbsapi/getpoint/index.html?qq-pf-to=pcqq.c2c"
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    driver = webdriver.Chrome('chromedriver',  chrome_options=chrome_options)
    driver.get(url)

    count = 0
    for a in addresses:
        driver.refresh()
        # if count<220:
        #     count+=1
        #     continue
        try:
            try:
                datas = find_geo_data(a,driver)
                write_line(datas)
            except:
                driver.refresh()
                print('尝试使用楼盘名称查找——')
                datas = find_geo_data(names[count],driver)
                write_line(datas)
        except:
            #print('尝试失败，插入[0,0]\t')
            #print('无法找到'+names[count])
            #print('\t'+count)
            datas = [0,0]
            write_line(datas)

        count+=1
    # driver.quit()

