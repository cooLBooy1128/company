'''
���ѡȡ100�����⳵��ʻ�켣��������Ϊtxt�ļ�
'''
import pandas as pd
import random


'''
��ȡ�ļ�Ϊdf��ʽ�����ѡȡ100�����⳵���ƺţ�����Ϊlist
'''
df=pd.read_csv(r'G:\���⳵\P_CZCGPS_20170403_sorted.txt',parse_dates=[2],encoding='utf8')
ser=df1.groupby(1).size()
l=random.choices(list(ser.index),k=100)


'''
�����ļ�f,����list�г��ƺ�ɸѡ��������������ļ�w��txt��ʽ��
'''
f=open(r'G:\���⳵\P_CZCGPS_20170403-20170409.txt',encoding='utf-8')
w=open(r'G:\���⳵\P_CZCGPS_100Car_20170403-20170409.txt','a',encoding='utf-8')
next(f) #ֱ��������һ��
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
��ȡ�����ļ�wΪdf��ʽ,���ݳ��ƺ���ʱ�����򣬲�����������ļ���txt��ʽ��
'''
df1=pd.read_csv(r'G:\���⳵\P_CZCGPS_100Car_20170403-20170409.txt',header=None,parse_dates=[2],encoding='utf8',dtype={9:str,10:str})
df2=df1.sort_values([1,2])
df2.to_csv(r'G:\���⳵\P_CZCGPS_100Car_20170403-20170409_sorted.txt',encoding='utf8',index=False)