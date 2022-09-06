import requests
import json
import random
import math
import os
import pandas as pd

'''
根据面积大小分批获取商铺json文件,每页20个json,最多100页
'''
def getby_area(area):
    try:
        i=1
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
                                    }
        url='https://api-crep.ke.com/ke/pu/list?cityId=610100&city=%E8%A5%BF%E5%AE%89&page=1&delType=2&diType=%E5%8C%BA%E5%9F%9F&area={}'.format(area)
        r=requests.get(url,headers=headers)
        dic=r.json()
        page=math.ceil(dic['data']['total']/20)
        if page>0:
            json.dump(r.json(),ensure_ascii=False,fp=open(r'G:\贝壳商业\西安市\商铺租赁\{}_1.json'.format(area),'w',encoding='utf8'))
            print(area,i)
            for i in range(2,page+1):
                url='https://api-crep.ke.com/ke/pu/list?cityId=610100&city=%E8%A5%BF%E5%AE%89&page={}&delType=2&diType=%E5%8C%BA%E5%9F%9F&area={}'.format(i,area)
                r=requests.get(url,headers=headers)
                json.dump(r.json(),ensure_ascii=False,fp=open(r'G:\贝壳商业\西安市\商铺租赁\{}_{}.json'.format(area,i),'w',encoding='utf8'))
                print(area,i)
                time.sleep(random.uniform(0,2))
    except Exception as e:
        print(e,area,i)
        with open(r'G:\贝壳商业\西安市\商铺租赁\temp_get_area.txt','a',encoding='utf8') as w:
            w.write(area,i,'\n')
            
            
def main1():
    if not os.path.exists(r'G:\贝壳商业\西安市\商铺租赁'):
        os.makedirs(r'G:\贝壳商业\西安市\商铺租赁')
    areas=['0-20','20-50','50-100','100-300','300-500','500-']
    for area in areas:
        getby_area(area)

main1()


'''
根据商铺json文件获取商铺id,并汇总
'''
def all_path(dirname,filt):
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
    
def getid(filename,writer):
    f=open(filename,'r',encoding='utf8')
    dic=json.load(f)
    docs=dic['data']['docs']
    for doc in docs:
        id=doc['houseCode']
        writer.write(str(id)+'\n')
    f.close()
        
def main2():        
    writer=open(r'G:\贝壳商业\西安市\商铺租赁\汇总.txt','a',encoding='utf8')
    writer.write('houseId\n')
    filt=['.json'] #设置过滤后的文件类型,可以设置多个类型
    result=all_path(r'G:\贝壳商业\西安市\商铺租赁',filt)
    for filename in result:
        getid(filename,writer)
    writer.close()
    df=pd.read_csv(r'G:\贝壳商业\西安市\商铺租赁\汇总.txt',encoding='utf8')
    df.drop_duplicates(inplace=True)
    df.to_csv(r'G:\贝壳商业\西安市\商铺租赁\汇总_去重.txt',encoding='utf8',index=False)
    
main2()


'''
根据商铺id,获取商铺详细信息
'''
def getby_id():
    df=pd.read_csv(r'G:\贝壳商业\西安市\商铺租赁\汇总_去重.txt',encoding='utf8')
    l=df['houseId'].to_list()
    try:
        for id in l:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
                'Referer': 'https://shangye.lianjia.com/xa/sp/rent/detail/{}'.format(id)
                                        }
                                        
            url='https://api-crep.ke.com/ke/pu/detail?id={}&cityId=610100'.format(id)
            r=requests.get(url,headers=headers)
            json.dump(r.json(),ensure_ascii=False,fp=open(r'G:\贝壳商业\西安市\商铺租赁\详细\{}.json'.format(id),'w',encoding='utf8'))
            print(id)
            time.sleep(random.uniform(0,0.5))
    except Exception as e:
        print(e,id)
        with open(r'G:\贝壳商业\西安市\商铺租赁\详细\temp_get_id.txt','a',encoding='utf8') as w:
            w.write(id,'\n')

getby_id()


'''
汇总商铺详细信息
'''
def all_path(dirname,filt):
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

    
def getdetail(filename,writer):
    try:
        with open(filename,'r',encoding='utf8') as f:
            dic=json.load(f)
        doc=dic['data']['docs']
        houseId=doc['houseCode']
        buildingName=doc['buildingName']
        totalPrice=doc['totalPrice']
        area=doc['area']
        singlePrice=doc['singlePrice']
        fitmentName=doc['fitmentName']
        if not fitmentName:
            fitmentName=''
        isStreetName=doc['isStreetName']
        cityName=doc['cityName']
        districtName=doc['districtName']
        streetName=doc['streetName']
        lon=doc['location']['lng']
        lat=doc['location']['lat']
        lon_gcj,lat_gcj=bd09_to_gcj02(lon, lat)
        lon_wgs,lat_wgs=bd09_to_wgs84(lon, lat)
        date=doc['ctime']['date']  
        writer.write(str(houseId)+','+buildingName+','+str(totalPrice)+','+str(area)+','+str(singlePrice)+','+fitmentName+','+isStreetName+','+cityName+','+districtName+','+streetName+','+str(lon)+','+str(lat)+','+str(round(lon_gcj,6))+','+str(round(lat_gcj,6))+','+str(round(lon_wgs,6))+','+str(round(lat_wgs,6))+','+date+'\n')
    except Exception as e:
        print(e,filename)


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

        
def main3():
    try:        
        writer=open(r'G:\贝壳商业\西安市\商铺租赁\详细\汇总.txt','a',encoding='utf8')
        writer.write('houseId,buildingName,totalPrice,area,singlePrice,fitmentName,floorTypeName,isStreetName,cityName,districtName,streetName,lon,lat,lon_gcj,lat_gcj,lon_wgs,lat_wgs,date\n')
        filt=['.json'] #设置过滤后的文件类型,可以设置多个类型
        result=all_path(r'G:\贝壳商业\西安市\商铺租赁\详细',filt)
        count=0
        for filename in result:
            count+=1
            if count%1000==0:
                print(count)
            getdetail(filename,writer)
    finally:
        writer.close()


PI = math.pi
PIX = math.pi * 3000 / 180
EE = 0.00669342162296594323
A = 6378245.0   
main3()













