#coding=gbk

import requests
from pyquery import PyQuery as pq
import re
import urllib.parse
import pandas as pd

def read_canmes(filename):
    df=pd.read_excel(filename)
    cnames=list(set(df['cname']))
    return cnames

def write_cnames(cnames,filename):
    df=pd.DataFrame(cnames,columns=['cname'])
    df.to_excel(filename,index=False)

def search(cname,filename,rest):
    try:
        #print('开始查询')
        headers1 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'referer':'https://www.qixin.com/search?key={}&page=1'.format(urllib.parse.quote(cname))
        }
        base_url='https://www.qixin.com/search?key={}'.format(urllib.parse.quote(cname))
        r1=requests.get(base_url,headers=headers1)
        p=pq(r1.text)
        if p('div.pull-left.small.font-14 em').text() == '0': #判断企业是否能搜索到
            print(cname,'有0条搜索结果')
        else:
            address=re.search('地址：(.*?)地图显示',p('div.legal-person span').text()).group(1)
            print('成功:',cname)
            with open(filename,'a',encoding='utf-8') as file:
                file.write(cname+','+address+'\n')
    except Exception as e:
        #print(e,cname)
        rest.append(cname) 
        
if __name__ == '__main__':  
    cnames=read_canmes(r'C:\Users\szu\Desktop\吉华街道项目\企业\企业数据爬虫\待爬企业名.xlsx')
    filename=r'C:\Users\szu\Desktop\吉华街道项目\企业\企业数据爬虫\吉华街道.txt'
    for i in range(1,21): #循环执行10次，将每次未成功爬取的企业名字记录到cnames中，便于再次查询
        rest=[]
        count=0
        for cname in cnames:
            count+=1
            if count%10==0:
                print(i,count)
            search(cname,filename,rest)
        cnames=rest
        write_cnames(cnames,r'C:\Users\szu\Desktop\吉华街道项目\企业\企业数据爬虫\待爬企业名.xlsx')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    