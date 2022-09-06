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
            address=r2.json()['data']['regAddr']
            industry=r2.json()['data']['industry']
            cname=r2.json()['data']['entName']
            shareholders=[]
            for i in r2.json()['data']['shares']:
                shareholders.append(i['name'])
            shareholder=';'.join(shareholders)
            url2='https://xin.baidu.com/detail/investajax?pid={}'.format(pid)
            r3=requests.get(url2,headers=headers2)
            invests=[]
            for i in r3.json()['data']['list']:
                #print(i['entName'])
                invests.append(i['entName'])
            invest=';'.join(invests)
            url3='https://xin.baidu.com/detail/branchajax?pid={}'.format(pid)
            r4=requests.get(url3,headers=headers2)
            branchs=[]
            for i in r4.json()['data']['list']:
                #print(i['entName'])
                branchs.append(i['entName'])
            branch=';'.join(branchs)           
            #print(cname+','+industry+','+shareholder+','+address+','+invest+','+branch)
            print('成功:',cname)
            with open(filename,'a',encoding='utf-8') as file:
                file.write(cname+','+industry+','+shareholder+','+address+','+invest+','+branch+'\n')
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
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    