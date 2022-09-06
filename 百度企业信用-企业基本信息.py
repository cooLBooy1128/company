import requests
from pyquery import PyQuery as pq
import re
import urllib.parse
import pandas as pd
import json
import time
import random

def read_canmes(filename):
    df=pd.read_excel(filename)
    cnames=list(df['cname'])
    return cnames

def write_cnames(cnames,filename):
    df=pd.DataFrame(cnames,columns=['cname'])
    df.to_excel(filename,index=False)

def search(cname,rest):
    try:
        #print('开始查询')
        headers1 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
        }
        base_url='https://xin.baidu.com/s?q={}&t=1'.format(urllib.parse.quote(cname))
        r1=requests.get(base_url,headers=headers1)
        p=pq(r1.text)
        if p('em.zx-result-counter').text() == '0': #判断企业是否能搜索到
            print(cname,'有0条搜索结果')
        else:
            pid=re.search('pid=(.*)',p('a.zx-list-item-url').attr('href')).group(1)
            headers2 = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
                'Referer': 'https://xin.baidu.com/detail/compinfo?pid={}'.format(pid),
                'X-Requested-With': 'XMLHttpRequest'
            }
            url1='https://xin.baidu.com/detail/basicAjax?pid={}'.format(pid)
            r2=requests.get(url1,headers=headers2)
            with open('G:\企业信息\企业基本信息\{}.json'.format(cname),'w',encoding='utf8') as f:
                json.dump(r2.json(),f,ensure_ascii=False) 
            time.sleep(random.uniform(1,2))
    except Exception as e:
        #print(e,cname)
        rest.append(cname) 
        
if __name__ == '__main__':  
    cnames=read_canmes(r'G:\企业信息\企业基本信息\待爬企业名.xlsx') #'待爬企业名.xlsx'为1列，列名为cname
    for i in range(1,21): #循环执行20次，将每次未成功爬取的企业名字记录到cnames中，便于再次查询
        rest=[]
        count=0
        for cname in cnames:
            count+=1
            if count%10==0:
                print(i,count)
            search(cname,rest)
        cnames=rest
        write_cnames(cnames,r'G:\企业信息\企业基本信息\待爬企业名.xlsx')
    