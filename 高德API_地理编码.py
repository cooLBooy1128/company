import pandas as pd
import requests
import urllib.parse

#调用接口示例 'https://restapi.amap.com/v3/geocode/geo?address=北京市朝阳区阜通东大街6号&output=XML&key=<用户的key>'
#结构化地址信息：国家、省份、城市、区县、城镇、乡村、街道、门牌号码、屋邨、大厦。
#如果需要解析多个地址的话，请用"|"进行间隔，并且将 batch 参数设置为 true，最多支持 10 个地址进进行"|"分割形式的请求。
#中文名	adcode citycode    深圳市 440300 0755；龙岗区 440307 0755


def get_addresses(filename):
    df=pd.read_csv(filename,header=None)
    addresses=[]
    adds=list(df[3].drop_duplicates().values)
    a=len(adds)//10
    b=len(adds)%10
    for i in range(a):
        address='|'.join(adds[i*10:i*10+10])
        addresses.append(address)
        #print(address)
    if b>0:
        address='|'.join(adds[-b:])
        addresses.append(address)
        #print(address)
    return addresses
        
def search_store(address,filename):
    try:
        address_list=address.split('|')
        writer=open(filename,'a',encoding='utf-8')
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
            }
        url='https://restapi.amap.com/v3/geocode/geo?address={}&key=86e677ba7863ae87c9b4a7be8fa0199f&batch=True'.format(urllib.parse.quote(address))
        r=requests.get(url,headers=headers)
        dic=r.json()
        if dic['status']=='1':    
            geocodes=dic['geocodes']
            i=0
            for geocode in geocodes:
                formatted_address=geocode['formatted_address']
                if formatted_address==[]:
                    formatted_address=''
                province=geocode['province']
                if province==[]:
                    province=''
                city=geocode['city']
                if city==[]:
                    city=''
                district=geocode['district']
                if district==[]:
                    district=''
                street=geocode['street']
                if street==[]:
                    street=''
                number=geocode['number']
                if number==[]:
                    number=''
                location=geocode['location']
                if location==[]:
                    location=''
                level=geocode['level']
                if level==[]:
                    level=''
                #print(formatted_address)
                #print(address_list[i]+'\t'+formatted_address+'\t'+province+'\t'+city+'\t'+district+'\t'+street+'\t'+number+'\t'+location+'\t'+level)        
                writer.write(address_list[i]+'\t'+formatted_address+'\t'+province+'\t'+city+'\t'+district+'\t'+street+'\t'+number+'\t'+location+'\t'+level+'\n')
                i+=1
    except Exception as e:
            print(e)
    finally:
        writer.close()
    
if __name__ == '__main__':
    f1=r'C:\Users\szu\Desktop\吉华街道项目\企业\企业数据爬虫\股东公司.txt'    
    f2=r'C:\Users\szu\Desktop\poi\股东公司地理编码.txt'
    addresses=get_addresses(f1)
    count=0    
    for address in addresses:
        search_store(address,f2)
        count+=10
        if count%20==0:
            print(count)
    
    
    
    
    
    
    
    