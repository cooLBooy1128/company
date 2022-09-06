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
        #print('��ʼ��ѯ')
        headers1 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'referer':'https://www.qixin.com/search?key={}&page=1'.format(urllib.parse.quote(cname))
        }
        base_url='https://www.qixin.com/search?key={}'.format(urllib.parse.quote(cname))
        r1=requests.get(base_url,headers=headers1)
        p=pq(r1.text)
        if p('div.pull-left.small.font-14 em').text() == '0': #�ж���ҵ�Ƿ���������
            print(cname,'��0���������')
        else:
            address=re.search('��ַ��(.*?)��ͼ��ʾ',p('div.legal-person span').text()).group(1)
            print('�ɹ�:',cname)
            with open(filename,'a',encoding='utf-8') as file:
                file.write(cname+','+address+'\n')
    except Exception as e:
        #print(e,cname)
        rest.append(cname) 
        
if __name__ == '__main__':  
    cnames=read_canmes(r'C:\Users\szu\Desktop\�����ֵ���Ŀ\��ҵ\��ҵ��������\������ҵ��.xlsx')
    filename=r'C:\Users\szu\Desktop\�����ֵ���Ŀ\��ҵ\��ҵ��������\�����ֵ�.txt'
    for i in range(1,21): #ѭ��ִ��10�Σ���ÿ��δ�ɹ���ȡ����ҵ���ּ�¼��cnames�У������ٴβ�ѯ
        rest=[]
        count=0
        for cname in cnames:
            count+=1
            if count%10==0:
                print(i,count)
            search(cname,filename,rest)
        cnames=rest
        write_cnames(cnames,r'C:\Users\szu\Desktop\�����ֵ���Ŀ\��ҵ\��ҵ��������\������ҵ��.xlsx')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    