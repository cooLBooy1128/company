import requests
import json
import time

#调用接口示例 'https://restapi.amap.com/v3/place/around?key=<用户的key>&location=116.473168,39.993015&radius=10000&types=011100'
#中文名	adcode citycode    深圳市 440300 0755；龙岗区 440307 0755
#060101 购物中心    120201 商务写字楼    190600 标志性建筑物

def store_json(city,types,page):
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
            }
    for i in range(1,page+1):
        print(i)
        url='https://restapi.amap.com/v3/place/around?key=86e677ba7863ae87c9b4a7be8fa0199f&location=114.128593,22.654069&keywords=&city={}&types={}&radius=50000&offset=50&page={}&extensions=all'.format(city,types,i)
        r=requests.get(url,headers=headers)
        json.dump(r.json(),ensure_ascii=False,fp=open(r'G:\深圳市商业综合体\{}.json'.format(i),'w',encoding='utf8'))
        time.sleep(1)

def get_csv(page,filename):
    writer=open(filename,'a',encoding='utf8')
    writer.write('id,name,type,typecode,address,location_lon,location_lat,business_area,pname,cityname,adname,entr_location_lon,entr_location_lat,navi_poiid\n')
    for j in range(1,page+1):
        f=open(r'G:\深圳市商业综合体\{}.json'.format(j),'r',encoding='utf8')
        dic=json.load(f)
        pois=dic['pois']
        count=0
        for poi in pois:
            count+=1
            if count%10==0:
                print(j,count)
            id_=poi['id']
            name=poi['name']
            type_=poi['type']
            typecode=poi['typecode']
            address=poi['address']
            if address==[]:
                address=''
            location=poi['location']
            pname=poi['pname']
            cityname=poi['cityname']
            adname=poi['adname']
            business_area=poi['business_area']
            if business_area==[]:
                business_area=''
            entr_location=poi['entr_location']
            if entr_location==[]:
                entr_location=','        
            navi_poiid=poi['navi_poiid']
            if navi_poiid==[]:
                navi_poiid=''
            #print(id_+','+name+','+type_+','+typecode+','+address+','+location+','+pname+','+cityname+','+adname+','+entr_location+','+navi_poiid)
            writer.write(id_+','+name+','+type_+','+typecode+','+address+','+location+','+business_area+','+pname+','+cityname+','+adname+','+entr_location+','+navi_poiid+'\n')
        f.close()
    writer.close()
        
if __name__ == '__main__': 
    filename=r'G:\深圳市商业综合体\SZ.txt'
    types=060101
    city=440300
    page=8
    store_json(city,types,page)
    get_csv(page,filename)

    
    
    
    
    
    
    
