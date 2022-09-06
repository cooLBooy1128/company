import requests
import random
import json
import time
import math
import os
from pyquery import PyQuery as pq
from bs4 import BeautifulSoup
import re
import pandas as pd


'''
获取基本信息,保存为HTML文件
'''
def getby_region_area(region,area):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
                    }
        url='https://xa.lianjia.com/chengjiao/{}/a{}/'.format(region,area)
        r=requests.get(url,headers=headers)
        soup=BeautifulSoup(r.text)
        with open(r'G:\链家二手房\西安市\成交\一级\{}_a{}_1.html'.format(region,area),'w',encoding='utf8') as w:
            w.write(soup.prettify())    
        p=pq(r.text)
        count=int(p('div.total.fl span').text())
        print(1,count)
        page=math.ceil(count/30)
        time.sleep(random.uniform(1,2))
        for i in range(2,page+1):
            print(i)
            url='https://xa.lianjia.com/chengjiao/{}/pg{}a{}/'.format(region,i,area) 
            r=requests.get(url,headers=headers)
            soup=BeautifulSoup(r.text)
            with open(r'G:\链家二手房\西安市\成交\一级\{}_a{}_{}.html'.format(region,area,i),'w',encoding='utf8') as w:
                w.write(soup.prettify())
            time.sleep(random.uniform(1,2))
    except Exception as e:
        print(e,region,area,i)
        with open(r'G:\链家二手房\西安市\成交\temp_get_region_area.txt','a',encoding='utf8') as w:
            w.write(region,area,i,'\n')

def main1():
    if not os.path.exists(r'G:\链家二手房\西安市\成交\一级'):
        os.makedirs(r'G:\链家二手房\西安市\成交\一级')
    regions=['beilin','weiyang','baqiao','xinchengqu','lintong','yanliang','changan4','lianhu','yanta','lantian','huyiqu','zhouzhi','gaoling1','xixianxinquxian']
    areas=range(1,9)
    for region in regions:
        for area in areas:
            print(region,area)
            getby_region_area(region,area)

main1()
    
    
'''
对获取到的HTML文件进行解析
'''
def all_path(dirname):
    result = []#所有的文件
    for maindir, subdir, file_name_list in os.walk(dirname):
        # print("1:",maindir) #当前主目录
        # print("2:",subdir) #当前主目录下的所有目录
        # print("3:",file_name_list)  #当前主目录下的所有文件
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)#合并成一个完整路径
            ext = os.path.splitext(apath)[1]  # 获取文件后缀,[0]获取的是除文件后缀名以外的内容          
            if ext in filt:
                result.append(apath)
                # print(os.path.splitext(apath)[0],os.path.splitext(apath)[1])
    return result

filt=['.html'] #设置过滤后的文件类型,可以设置多个类型
result=all_path(r'G:\链家二手房\西安市\成交\一级')
writer=open(r'G:\链家二手房\西安市\成交\一级\汇总.txt','a',encoding='utf8')
writer.write('hid,houseInfo,title,dealDate,totalPrice,positionInfo,unitPrice,dealCycleeInfo1,dealCycleeInfo2,link\n')
count=0
for file in result:
    count+=1
    if count%50==0:
        print(count)
    with open(file,'r',encoding='utf8') as f:
        p=pq(f.read())
    for i in range(1,31):
        if p('li:nth-child({}) div.title a'.format(i))==[]:
            break
        link=p('li:nth-child({}) div.title a'.format(i)).attr('href')
        hid=re.search('(\d+).html',link).group(1)
        houseInfo=p('li:nth-child({}) div.houseInfo'.format(i)).text()
        title=p('li:nth-child({}) div.title a'.format(i)).text()
        dealDate=p('li:nth-child({}) div.dealDate'.format(i)).text()
        totalPrice=p('li:nth-child({}) div.totalPrice'.format(i)).text()
        positionInfo=p('li:nth-child({}) div.positionInfo'.format(i)).text()
        unitPrice=p('li:nth-child({}) div.unitPrice'.format(i)).text()
        dealCycleeInfo1=p('li:nth-child({}) span.dealCycleTxt span:nth-child(1)'.format(i)).text()
        dealCycleeInfo2=p('li:nth-child({}) span.dealCycleTxt span:nth-child(2)'.format(i)).text()
        writer.write(hid+','+title+','+houseInfo+','+dealDate+','+totalPrice+','+positionInfo+','+unitPrice+','+dealCycleeInfo1+','+dealCycleeInfo2+','+link+'\n')
    f.close()
writer.close()

'''
对汇总文件去重
'''
df=pd.read_csv(r'G:\链家二手房\西安市\成交\一级\汇总.txt',encoding='utf8')
df.drop_duplicated(inplace=True)
df.to_csv(r'G:\链家二手房\西安市\成交\一级\汇总.txt',encoding='utf8',index=False)

 
'''
根据link获取rid
'''
def getby_link(link,writer):
    try:
        headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
                    'X-Requested-With': 'XMLHttpRequest'
                            }
        r=requests.get(link,headers=headers)
        soup=BeautifulSoup(r.text)
        hid=re.search('(\d+).html',link).group(1)
        with open(r'G:\链家二手房\西安市\成交\二级\{}.html'.format(hid),'w',encoding='utf8') as w:
            w.write(soup.prettify())    
        p=pq(r.text)
        rid=p('div.house-title').attr('data-lj_action_housedel_id')
        writer.write(hid+','+rid+'\n')
    except Exception as e:
        print(e,link)
        with open(r'G:\链家二手房\西安市\成交\temp_link.txt','a',encoding='utf8') as w:
            w.write(link+'\n')
 
def main2():
    if not os.path.exists(r'G:\链家二手房\西安市\成交\二级'):
        os.makedirs(r'G:\链家二手房\西安市\成交\二级')
    writer=open(r'G:\链家二手房\西安市\成交\hid_rid.txt','a',encoding='utf8')
    writer.write('hid,rid\n')
    df=pd.read_csv(r'G:\链家二手房\西安市\成交\一级\汇总.txt',encoding='utf8')
    links=df['link'].tolist()
    count=0
    for link in links:
        count+=1
        if count%50==0:
            print(count)
        getby_link(link,writer)
        time.sleep(random.uniform(0,1))
    writer.close()

main2()


'''
根据hid和rid获取百度地图经纬度坐标 例：https://xa.lianjia.com/ershoufang/housestat?hid=101104022007&rid=3811059392402
'''
def getby_hid_rid(hid,rid,writer):
    try:
        headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
                    'X-Requested-With': 'XMLHttpRequest'
                            }
        url='https://xa.lianjia.com/ershoufang/housestat?hid={}&rid={}'.format(hid,rid)
        r=requests.get(url,headers=headers)
        dic=r.json()
        location=dic['data']['resblockPosition']
        writer.write(hid+','+location+'\n')
    except Exception as e:
        print(e,hid,uid)
        with open(r'G:\链家二手房\西安市\成交\temp_hid_rid.txt','a',encoding='utf8') as w:
            w.write(hid+','+uid+'\n')
 
def main3():
    writer=open(r'G:\链家二手房\西安市\成交\百度地图经纬度.txt','a',encoding='utf8')
    writer.write('hid,lon,lat\n')
    df=pd.read_csv(r'G:\链家二手房\西安市\成交\hid_rid.txt',encoding='utf8')
    hrid=df[['hid','rid']].tolist()
    count=0
    for hid,rid in hrid:
        count+=1
        if count%50==0:
            print(count)
        getby_hid_rid(hid,rid,writer)
        #time.sleep(random.uniform(0,1))
    writer.close()

main3()


'''
根据link获取rid，再获取百度地图经纬度坐标 
'''
def getby_link1(link,writer1,writer2):
    try:
        headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
                    'X-Requested-With': 'XMLHttpRequest'
                            }
        r=requests.get(link,headers=headers)
        soup=BeautifulSoup(r.text)
        hid=re.search('(\d+).html',link).group(1)
        with open(r'G:\链家二手房\西安市\成交\二级\{}.html'.format(hid),'w',encoding='utf8') as w:
            w.write(soup.prettify())    
        p=pq(r.text)
        rid=p('div.house-title').attr('data-lj_action_housedel_id')
        writer1.write(hid+','+rid+'\n')
        getby_hid_rid(hid,rid,writer2)
    except Exception as e:
        print(e,link)
        with open(r'G:\链家二手房\西安市\成交\temp_link.txt','a',encoding='utf8') as w:
            w.write(link+'\n')
 
def main4():
    if not os.path.exists(r'G:\链家二手房\西安市\成交\二级'):
        os.makedirs(r'G:\链家二手房\西安市\成交\二级')
    writer1=open(r'G:\链家二手房\西安市\成交\hid_rid.txt','a',encoding='utf8')
    writer1.write('hid,rid\n')
    writer2=open(r'G:\链家二手房\西安市\成交\百度地图经纬度.txt','a',encoding='utf8')
    writer2.write('hid,lon,lat\n')
    df=pd.read_csv(r'G:\链家二手房\西安市\成交\一级\汇总.txt',encoding='utf8')
    links=df['link'].tolist()
    count=0
    for link in links:
        count+=1
        if count%50==0:
            print(count)
        getby_link1(link,writer1,writer2)
        #time.sleep(random.uniform(0,1))
    writer1.close()
    writer2.close()

main4()


'''
合并、整理成交二手房信息
'''
def bd09_to_gcj02(lng, lat):
    """BD09 -> GCJ02"""
    x, y =  lng - 0.0065, lat - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * PIX)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * PIX)
    lng, lat = z * math.cos(theta), z * math.sin(theta)
    return lng, lat
 
 
def gcj02_to_wgs84(lng, lat):
    """GCJ02 -> WGS84"""
    if out_of_china(lng, lat):
        return lng, lat
    dlat = transform_lat(lng - 105.0, lat - 35.0)
    dlng = transform_lng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * PI
    magic = math.sin(radlat)
    magic = 1 - EE * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((A * (1 - EE)) / (magic * sqrtmagic) * PI)
    dlng = (dlng * 180.0) / (A / sqrtmagic * math.cos(radlat) * PI)
    lng, lat = lng - dlng, lat - dlat
    return lng,lat


def transform_lat(lng, lat):
    """GCJ02 latitude transformation"""
    ret = -100 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + 0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * PI) + 20.0 * math.sin(2.0 * lng * PI)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * PI) + 40.0 * math.sin(lat / 3.0 * PI)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * PI) + 320.0 * math.sin(lat * PI / 30.0)) * 2.0 / 3.0
    return ret


def transform_lng(lng, lat):
    """GCJ02 longtitude transformation"""
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + 0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * PI) + 20.0 * math.sin(2.0 * lng * PI)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * PI) + 40.0 * math.sin(lng / 3.0 * PI)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * PI) + 300.0 * math.sin(lng / 30.0 * PI)) * 2.0 / 3.0
    return ret
    
    
def out_of_china(lng, lat):
    """No offset when coordinate out of China."""
    if lng < 72.004 or lng > 137.8437:
        return True
    if lat < 0.8293 or lat > 55.8271:
        return True
    return False


def bd09_to_wgs84(lng, lat):
    """BD09 -> WGS84"""
    lng, lat = bd09_to_gcj02(lng, lat)
    lng, lat = gcj02_to_wgs84(lng, lat)
    return lng, lat

        
def main5():
    df=pd.read_csv(r'G:\链家二手房\西安市\成交\一级\汇总.txt',encoding='utf8')  
    dfa=pd.read_csv(r'G:\链家二手房\西安市\成交\hid_rid.txt',encoding='utf8')
    writer=open(r'G:\链家二手房\西安市\成交\百度地图经纬度_坐标转换.txt','a',encoding='utf8')
    writer.write('hid,lon,lat,lon_gcj,lat_gcj,lon_wgs,lat_wgs\n')
    with open(r'G:\链家二手房\西安市\成交\百度地图经纬度.txt','r',encoding='utf8') as f:
        next(f)
        for row in f:
            l=row.split(',')
            lon=l[1]
            lat=l[2].strip()
            lon_gcj,lat_gcj=bd09_to_gcj02(float(lon), float(lat))
            lon_wgs,lat_wgs=bd09_to_wgs84(float(lon), float(lat))
            writer.write(row.strip()+','+str(round(lon_gcj,6))+','+str(round(lat_gcj,6))+','+str(round(lon_wgs,6))+','+str(round(lat_wgs,6))+'\n')
    writer.close()
    dfb=pd.read_csv(r'G:\链家二手房\西安市\成交\百度地图经纬度_坐标转换.txt',encoding='utf8')
    df1=pd.merge(df,dfa,on='hid')
    df2=pd.merge(df1,dfb,on='hid')
    df2.to_csv(r'G:\链家二手房\西安市\成交\汇总_合并经纬度.txt',encoding='utf8',index=False)
    
       
PI = math.pi
PIX = math.pi * 3000 / 180
EE = 0.00669342162296594323
A = 6378245.0   
main5()


'''
从“汇总_合并经纬度”文件中提取所需信息
'''
df=pd.read_csv(r'G:\链家二手房\西安市\成交\汇总_合并经纬度.txt',encoding='utf8')
df1=df[~df['houseInfo'].str.contains(' 车位')]
df1.loc[:,'area']=df1.loc[:,'houseInfo'].str.split(' ').apply(lambda x:float(x[-1][:-2]))
df1.loc[:,'totalPrice_num']=df1.loc[:,'totalPrice'].str[:-1].astype(int)
df1.loc[:,'unitPrice_num']=df1.loc[:,'unitPrice'].str[:-3].astype(int)




