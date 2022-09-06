import pandas as pd
import requests
import urllib.parse
import json

#在此接口之中，您可以通过city&citylimit参数指定希望搜索的城市或区县。而city参数能够接收citycode和adcode，citycode仅能精确到城市，而adcode却能够精确到区县。无论指定多少个type，每次请求最多返回1000个POI信息。
#调用接口示例 'https://restapi.amap.com/v3/place/text?keywords=北京大学&city=beijing&output=xml&offset=20&page=1&key=<用户的key>&extensions=all'
#中文名	adcode citycode    深圳市 440300 0755；龙岗区 440307 0755
'''
NEW_TYPE	大类	中类	小类
170000  公司企业	公司企业	公司企业
170100	公司企业	知名企业	知名企业
170200	公司企业	公司	公司
170201	公司企业	公司	广告装饰
170202	公司企业	公司	建筑公司
170203	公司企业	公司	医药公司
170204	公司企业	公司	机械电子
170205	公司企业	公司	冶金化工
170206	公司企业	公司	网络科技
170207	公司企业	公司	商业贸易
170208	公司企业	公司	电信公司
170209	公司企业	公司	矿产公司
170300	公司企业	工厂	工厂
170400	公司企业	农林牧渔基地	其它农林牧渔基地
170401	公司企业	农林牧渔基地	渔场
170402	公司企业	农林牧渔基地	农场
170403	公司企业	农林牧渔基地	林场
170404	公司企业	农林牧渔基地	牧场
170405	公司企业	农林牧渔基地	家禽养殖基地
170406	公司企业	农林牧渔基地	蔬菜基地
170407	公司企业	农林牧渔基地	水果基地
170408	公司企业	农林牧渔基地	花卉苗圃基地
'''

def get_adcode(filename,sheetname):
    df=pd.read_excel(filename,sheet_name=sheetname,converters={'citycode':str,'adcode':str})
    adcodes=df['adcode'].values.tolist()
    return adcodes

def get_poicode(filename,sheetname):
    df=pd.read_excel(filename,sheet_name=sheetname,converters={'NEW_TYPE':str})
    poicodes=df['NEW_TYPE'].values.tolist()
    return poicodes

def search(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
        }
    r=requests.get(url,headers=headers)
    dic=r.json()
    return dic

def store(dic,filename):
    try:
        writer=open(filename,'a',encoding='utf-8')
        if dic['status']=='1':    
            pois=dic['pois']
            count=0
            for poi in pois:
                count+=1
                print(count)
                id=poi['id']
                name=poi['name']
                type=poi['type']
                typecode=poi['typecode']
                address=poi['address']
                if address==[]:
                    address=''
                location=poi['location']
                pname=poi['pname']
                cityname=poi['cityname']
                adname=poi['adname']
                entr_location=poi['entr_location']
                if entr_location==[]:
                    entr_location=''        
                navi_poiid=poi['navi_poiid']
                if navi_poiid==[]:
                    navi_poiid=''
                #print(id+'\t'+name+'\t'+type+'\t'+typecode+'\t'+address+'\t'+location+'\t'+pname+'\t'+cityname+'\t'+adname+'\t'+entr_location+'\t'+navi_poiid)
                writer.write(id+'\t'+name+'\t'+type+'\t'+typecode+'\t'+address+'\t'+location+'\t'+pname+'\t'+cityname+'\t'+adname+'\t'+entr_location+'\t'+navi_poiid+'\n')
    except Exception as e:
            print(e)
    finally:
        writer.close()
    
    
def main(types,city,f):
    url='https://restapi.amap.com/v3/place/text?key=86e677ba7863ae87c9b4a7be8fa0199f&types={}&city={}&citylimit=True&children=1&offset=50&page=1&extensions=all'.format(types,city)
    dic=search(url)
    print('第1页')
    store(dic,f)
    if dic['status']=='1': 
        count=int(dic['count'])
        page_end=count//50+1
        for i in range(2,page_end+1):
            url='https://restapi.amap.com/v3/place/text?key=86e677ba7863ae87c9b4a7be8fa0199f&types={}&city={}&citylimit=True&children=1&offset=50&page={}&extensions=all'.format(types,city,i)
            dic=search(url) 
            print('第'+str(i)+'页')
            store(dic,f)

def main1(poicode,adcode,folder):
    url='https://restapi.amap.com/v3/place/text?key=86e677ba7863ae87c9b4a7be8fa0199f&types={}&city={}&citylimit=True&children=1&offset=50&page=1&extensions=all'.format(poicode,adcode)
    dic=search(url)
    print('第1页')
    json.dump(dic,open(folder+r'\{}_{}_1.json'.format(adcode,poicode),'w',encoding='utf8'),ensure_ascii=False)
    if dic['status']=='1': 
        count=int(dic['count'])
        page_end=count//50+1
        for i in range(2,page_end+1):
            url='https://restapi.amap.com/v3/place/text?key=86e677ba7863ae87c9b4a7be8fa0199f&types={}&city={}&citylimit=True&children=1&offset=50&page={}&extensions=all'.format(poicode,adcode,i)
            dic=search(url) 
            print('第'+str(i)+'页')
            json.dump(dic,open(folder+r'\{}_{}_{}.json'.format(adcode,poicode,i),'w',encoding='utf8'),ensure_ascii=False)

def main2(poicode,adcode,folder,key,totalcount):
    try:
        url='https://restapi.amap.com/v3/place/text?key={}&types={}&city={}&citylimit=True&children=1&offset=50&page=1&extensions=all'.format(key,poicode,adcode)
        dic=search(url)
        #print('第1页')
        json.dump(dic,open(folder+r'\{}_{}_1.json'.format(adcode,poicode),'w',encoding='utf8'),ensure_ascii=False)
        count=int(dic['count'])
        page_end=count//50+1
        totalcount=page_end
        for i in range(2,page_end+1):
            url='https://restapi.amap.com/v3/place/text?key={}&types={}&city={}&citylimit=True&children=1&offset=50&page={}&extensions=all'.format(key,poicode,adcode,i)
            dic=search(url) 
            #print('第'+str(i)+'页')
            json.dump(dic,open(folder+r'\{}_{}_{}.json'.format(adcode,poicode,i),'w',encoding='utf8'),ensure_ascii=False)      
    except Exception as e:
        print(e,adcode,poicode)
        totalcount=0
        with open(r'G:\高德poi\rest2.txt','a',encoding='utf8') as w:
            w.write(adcode+','+poicode+'\n')
    finally:
        return totalcount
    
    
    
if __name__ == '__main__':
    folderid=2
    folder=r'G:\高德poi\中国{}'.format(folderid)
    adcodes=get_adcode(r'G:\高德poi\AMap_adcode_citycode.xlsx','ad1')
    poicodes=get_poicode(r'G:\高德poi\amap_poicode.xlsx',2)
    totalcount=0
    keylist=['50f78e8f96c9f3cec2dd37bdb65d8315','4559465164415b35e6cb677a9539f92d','b838374d3c8bd9bba3ba5368d032bd04','7f10a9474ce94dba0fe0d7055b40c8b3','7caca3381b5cebcc2033499b1ee10531']
    keyid=0
    key=keylist[keyid]
    for adcode in adcodes:
        for poicode in poicodes:
            tempcount=main2(poicode,adcode,folder,key,totalcount) 
            totalcount+=tempcount
            if totalcount%100==0:
                print(totalcount)
            if totalcount>299000:
                keyid+=1
                if keyid>4:
                    keyid=0
                totalcount=0
                folderid+=1
                folder=r'G:\高德poi\中国{}'.format(folderid)
                key=keylist[keyid]

    