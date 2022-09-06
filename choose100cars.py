'''
随机选取100辆出租车行驶轨迹，并保存为txt文件
'''
import pandas as pd
import random


'''
读取文件为df格式，随机选取100辆出租车车牌号，保存为list
'''
df=pd.read_csv(r'G:\出租车\P_CZCGPS_20170403_sorted.txt',parse_dates=[2],encoding='utf8')
ser=df1.groupby(1).size()
l=random.choices(list(ser.index),k=100)


'''
遍历文件f,根据list中车牌号筛选，并将结果存入文件w（txt格式）
'''
f=open(r'G:\出租车\P_CZCGPS_20170403-20170409.txt',encoding='utf-8')
w=open(r'G:\出租车\P_CZCGPS_100Car_20170403-20170409.txt','a',encoding='utf-8')
next(f) #直接跳过第一行
count=0
for msg in f:
    count+=1
    if count%500000==0:
        print(count)
    recentname=msg.split(',')[1]
    if recentname in l:
        w.write(msg)
w.close()
f.close()

'''
读取上述文件w为df格式,根据车牌号与时间排序，并将结果存入文件（txt格式）
'''
df1=pd.read_csv(r'G:\出租车\P_CZCGPS_100Car_20170403-20170409.txt',header=None,parse_dates=[2],encoding='utf8',dtype={9:str,10:str})
df2=df1.sort_values([1,2])
df2.to_csv(r'G:\出租车\P_CZCGPS_100Car_20170403-20170409_sorted.txt',encoding='utf8',index=False)