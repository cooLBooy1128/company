import requests
import random
import json
import time
import math
import os

'''
获取基本信息
'''
url='http://www.winshangdata.com/wsapi/project/list3_4'
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'Referer': 'http://www.winshangdata.com/projectList'
        }
for i in range(1,18):
    print(i)
    data={"pageNum":i,"orderBy":"1","pageSize":60,"zsxq_yt1":"","zsxq_yt2":"","qy_p":319,"qy_c":602,"qy_a":"","xmzt":"","key":"","wuyelx":"","isHaveLink":"","ifdporyt":""}
    r=requests.post(url,headers=headers,json=data)
    json.dump(r.json(),ensure_ascii=False,fp=open(r'G:\深圳市商业综合体\深圳市商业项目_赢商大数据\项目基本信息\{}.json'.format(i),'w',encoding='utf8'))

    
'''
汇总基本信息
'''
filename='G:\深圳市商业综合体\深圳市商业项目_赢商大数据\项目基本信息\汇总.txt'
writer=open(filename,'a',encoding='utf8')
writer.write('projectId\tprojectName\txmZhuangTai\twuYeLx\twuYeLxID\tkaiYeShiJian\tkaiYeShiJianReal\tshangYeMianji\tzhaoShangXQ\n')
for i in range(1,18):
    print(i)
    f=open(r'G:\深圳市商业综合体\深圳市商业项目_赢商大数据\项目基本信息\{}.json'.format(i),encoding='utf8')
    dic=json.load(f)
    ls=dic['data']['list']
    for prj in ls:
        projectId=prj['projectId']
        projectName=prj['projectName']
        xmZhuangTai=prj['xmZhuangTai']
        wuYeLx=prj['wuYeLx']
        wuYeLxID=prj['wuYeLxID']
        kaiYeShiJian=prj['kaiYeShiJian']
        kaiYeShiJianReal=prj['kaiYeShiJianReal']
        shangYeMianji=prj['shangYeMianji']
        zhaoShangXQ=prj['zhaoShangXQ']
        writer.write(str(projectId)+'\t'+projectName+'\t'+str(xmZhuangTai)+'\t'+wuYeLx+'\t'+wuYeLxID+'\t'+kaiYeShiJian+'\t'+kaiYeShiJianReal+'\t'+str(shangYeMianji)+'\t'+zhaoShangXQ+'\n')
    f.close()
writer.close()   
    
    
'''
获取地址信息
'''
rest=[]
url='http://www.winshangdata.com/api/ProjectMapApi.aspx'
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'Referer': 'http://www.winshangdata.com/map/mapmin.html',
        'X-Requested-With': 'XMLHttpRequest'
        }
f=open('G:\深圳市商业综合体\深圳市商业项目_赢商大数据\项目基本信息\汇总.txt',encoding='utf8')
next(f)
for row in f:
    try:
        l=row.split('\t')
        #print(l[0])
        data={'action':'getdetailformap','id':l[0]}
        r=requests.post(url,headers=headers,data=data)
        json.dump(r.json(),ensure_ascii=False,fp=open(r'G:\深圳市商业综合体\深圳市商业项目_赢商大数据\项目地址\{}.json'.format(l[0]),'w',encoding='utf8'))
        print(l[0])
        time.sleep(random.uniform(0,5)/10)
    except Exception as e:
        print(e,l[0])
        rest.append(l[0])
    
    
'''
汇总地址信息
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

PI = math.pi
PIX = math.pi * 3000 / 180
EE = 0.00669342162296594323
A = 6378245.0
filt=['.json'] #设置过滤后的文件类型,可以设置多个类型
result=all_path(r'G:\深圳市商业综合体\深圳市商业项目_赢商大数据\项目地址')
filename='G:\深圳市商业综合体\深圳市商业项目_赢商大数据\项目地址\汇总.txt'
writer=open(filename,'a',encoding='utf8')
writer.write('ID\tName\tArea\tLng\tLat\tOpenTime\tType\tRemark\tCityName\tAddress\tStatu\tLng_wgs\tLat_wgs\n')
for filename in result:
    f=open(filename,encoding='utf8')
    dic=json.load(f)
    prj=dic['data']
    ID=prj['ID']
    Name=prj['Name']
    Area=prj['Area']
    Lng=prj['Lng']
    Lat=prj['Lat']
    temp=gcj02_to_wgs84(Lng,Lat)
    Lng_wgs=round(temp[0],6)
    Lat_wgs=round(temp[1],6)
    OpenTime=prj['OpenTime']
    Type=prj['Type']
    Remark=prj['Remark']
    CityName=prj['CityName']
    Address=prj['Address']
    Statu=prj['Statu']
    writer.write(ID+'\t'+Name+'\t'+Area+'\t'+str(Lng)+'\t'+str(Lat)+'\t'+OpenTime+'\t'+Type+'\t'+Remark+'\t'+CityName+'\t'+Address+'\t'+Statu+'\t'+str(Lng_wgs)+'\t'+str(Lat_wgs)+'\n')
    f.close()
writer.close()





















