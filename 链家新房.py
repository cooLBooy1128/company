import requests
import random
import json
import time
import math
import os

'''
获取基本信息
'''
if not os.path.exists(r'G:\链家新房\西安市'):
    os.makedirs(r'G:\链家新房\西安市')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'Referer': 'https://sz.fang.lianjia.com/loupan/',
    'X-Requested-With': 'XMLHttpRequest'
            }
for i in range(1,130):
    print(i)
    #URL中dg指东莞，sz指深圳，xa指西安；i指页数，每页有10个项目
    url='https://xa.fang.lianjia.com/loupan/pg{}/?_t=1'.format(i) 
    r=requests.get(url,headers=headers)
    json.dump(r.json(),ensure_ascii=False,fp=open(r'G:\链家新房\西安市\{}.json'.format(i),'w',encoding='utf8'))
    time.sleep(random.uniform(2,5))


'''
根据获取到的json文件汇总基本信息
'''
filename='G:\链家新房\东莞市\汇总.txt'
writer=open(filename,'a',encoding='utf8')
writer.write('projectId\tprojectName\txmZhuangTai\twuYeLx\twuYeLxID\tkaiYeShiJian\tkaiYeShiJianReal\tshangYeMianji\tzhaoShangXQ\n')
for i in range(1,44):
    print(i)
    f=open(r'G:\链家新房\东莞市\{}.json'.format(i),encoding='utf8')
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
    
 





















