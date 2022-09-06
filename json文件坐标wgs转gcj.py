import json 
import math


PI = math.pi
PIX = math.pi * 3000 / 180
EE = 0.00669342162296594323
A = 6378245.0


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

    
def wgs84_to_gcj02(lng, lat):
    """WGS84 -> GCJ02"""
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
    lng, lat = lng + dlng, lat + dlat
    return lng,lat

def get_gcj02(s):
    lng=float(s.split('|')[0].split(',')[0])
    lat=float(s.split('|')[0].split(',')[1])
    lng_gcj,lat_gcj=wgs84_to_gcj02(lng, lat)
    return str(round(lng_gcj,6))+','+str(round(lat_gcj,6))+'|12'


if __name__=='__main__':
    with open(r'C:\Users\cooLBoy\Desktop\bundle.json','r',encoding='utf8') as f:
        dic=json.load(f)
    provinces=dic['provinces']
    for i in provinces:
        #print(i['g'])
        i['g']=get_gcj02(i['g'])
        cities=i['cities']
        for j in cities:
            #print(j['n'],j['g'])
            j['g']=get_gcj02(j['g'])
    with open(r'C:\Users\cooLBoy\Desktop\bundle_gcj02.json','w',encoding='utf8') as f:
        json.dump(dic,f,ensure_ascii=False)

