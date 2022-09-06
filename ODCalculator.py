import pandas as pd
import numpy as np
import time

'''
将原文件转换为TRADETYPE为21、22，并根据时间排序好的文件 '_sorted'
'''
def sortfiles(filename,dfs):
    df=pd.read_csv('E:\\国土局（2013-2018）\\2018\\{}.tsv'.format(filename),sep='\t',header=0,parse_dates=['TRADEDATE'])
    df1=df[df.TRADETYPE.isin([21,22])]
    df1['STATIONID']=df1['TERMINALID'].map(lambda x:int(str(x)[:6]))
    df2=pd.merge(df1,dfs,on='STATIONID',how='left')
    df3=df2.sort_values(by=['CARDID','TRADEDATE'])
    df3.to_csv('E:\\国土局（2013-2018）\\2018\\{}_sorted.txt'.format(filename),sep='\t',encoding='utf_8_sig',header=True,index=False)

dfs=pd.read_csv('E:\\Project\\Metro\\Metro_Data\\station.txt',sep='\t',encoding='gbk',header=None,names=['STATIONID','STATIONNAME'])
filename='20180101-20180107'
sortfiles(filename,dfs)


################################################################
'''
直接使用pandas中的dataframe数据结构，通过遍历每行实现上述文件 '_sorted' 的筛选与两行的合并
但速度较慢，遍历10000行需要32s左右
'''
s1=df3.groupby('CARDID').size()
df5=pd.DataFrame(columns=('CARDID','TRADETYPE_x','TRADEDATE_x','TERMINALID_x','STATIONID_x','STATIONNAME_x','TRADETYPE_y','TRADEDATE_y','TERMINALID_y','STATIONID_y','STATIONNAME_y'))
count=0

start=time.clock()
count=0
df5=pd.DataFrame(columns=('CARDID','TRADETYPE_x','TRADEDATE_x','TERMINALID_x','STATIONID_x','STATIONNAME_x','TRADETYPE_y','TRADEDATE_y','TERMINALID_y','STATIONID_y','STATIONNAME_y'))
for j in s1.index[:1000]:
	count+=1
    print('第'+str(count)+'个CARDID')
    df4=df3[df3.CARDID==j]
	i=0
	while i < len(df4)-1:
        if df4.iloc[i].TRADETYPE==21 and df4.iloc[i+1].TRADETYPE==22:
            temp=pd.merge(df4.iloc[i].to_frame().T,df4.iloc[i+1].to_frame().T,on='CARDID')
            df5=df5.append(temp,ignore_index=True)
			i+=2
		else:
			i+=1
end=time.clock()
print('Running time:',end-start)
			
df5.to_csv('E:\\Project\\Metro\\Metro_Data\\同卡号出行轨迹_20000000-294000000.txt', sep='\t', header=True,index=False)

for j in range(1,8):
    for i in range(24):
        df6=df5[(df5.TRADEDATE_x>='2018-01-{} {}:00:00'.format(str(j).rjust(2,'0'),str(i).rjust(2,'0')))&(df5.TRADEDATE_x<'2018-01-01 {}:00:00'.format(str(j).rjust(2,'0'),str(i+1).rjust(2,'0')))]
        sr=df6.groupby(['STATIONNAME_x','STATIONNAME_y']).size()
        sr.name='出行OD'
        sr.reset_index().to_csv('E:\\Project\\Metro\\Metro_Data\\出行OD_20000000-294000000_2018-01-{}-{}_2018-01-{}-{}.txt'.format(str(j).rjust(2,'0'),str(i).rjust(2,'0'),str(j).rjust(2,'0'),str(i+1).rjust(2,'0'))), sep='\t', header=True,index=False)
		

		
		
start=time.clock()
count=0
df5=pd.DataFrame()
for j in s1.index[:1000]:
	count+=1
    print('第'+str(count)+'个CARDID')
    df4=df3[df3.CARDID==j]
	i=0
	while i < len(df4)-1:
		startpoint=df4.iloc[i]
		endpoint=df4.iloc[i+1]
        if startpoint.TRADETYPE==21 and endpoint.TRADETYPE==22:
			temp=startpoint.append(endpoint,ignore_index=True)
            df5=df5.append(temp,ignore_index=True)
			i+=2
		else:
			i+=1
end=time.clock()
print('Running time:',end-start)


start=time.clock()
count=0
df5=pd.DataFrame(columns=('CARDID','TRADETYPE_x','TRADEDATE_x','TERMINALID_x','STATIONID_x','STATIONNAME_x','TRADETYPE_y','TRADEDATE_y','TERMINALID_y','STATIONID_y','STATIONNAME_y'))
for j in s1.index[:1000]:
	count+=1
    print('第'+str(count)+'个CARDID')
    df4=df3[df3.CARDID==j]
	i=0
	while i < len(df4)-1:
		startpoint=df4.iloc[i]
		endpoint=df4.iloc[i+1]
        if startpoint.TRADETYPE==21 and endpoint.TRADETYPE==22:
			temp=pd.merge(startpoint.to_frame().T,endpoint.to_frame().T,on='CARDID')
            df5=df5.append(temp,ignore_index=True)
			i+=2
		else:
			i+=1
end=time.clock()
print('Running time:',end-start)


start=time.clock()
count=0
df5=pd.DataFrame(columns=('CARDID','TRADETYPE_x','TRADEDATE_x','TERMINALID_x','STATIONID_x','STATIONNAME_x','TRADETYPE_y','TRADEDATE_y','TERMINALID_y','STATIONID_y','STATIONNAME_y'))
i=0
while i < 10000:
    print('第'+str(i)+'行')
	startpoint=df3.iloc[i]
	endpoint=df3.iloc[i+1]
    if startpoint.CARDID==endpoint.CARDID and startpoint.TRADETYPE==21 and endpoint.TRADETYPE==22:
		temp=pd.merge(startpoint.to_frame().T,endpoint.to_frame().T,on='CARDID')
        df5=df5.append(temp,ignore_index=True)
		i+=2
	else:
		i+=1
end=time.clock()
print('Running time:',end-start)

################################################################
'''
直接遍历文件 '_sorted' 读取字符流 ，并将筛选合并后的字符串存入新文件 'Metro_Statistics_OD_'
速度很快，处理整个文件（4000多万行）约200s
'''

'''
使用with语句会多次自动关闭文件，使速度变慢

start=time.clock()
with open('E:\\Project\\Metro\\Metro_Data\\20180101-20180107_sorted.txt',encoding='utf-8') as f:
    next(f) #直接跳过第一行
    count=0
    for msg in f:
        count+=1
        if count%10000==0:
            print(count)
        recentcid=msg.split('\t')[0]
        recenttype=msg.split('\t')[1]
        recenttime=msg.split('\t')[2]
        recentsid=msg.split('\t')[4]
        recentsname=msg.split('\t')[5].strip()
        if recentcid==precid and pretype=='21' and recenttype=='22':
            with open('E:\\Project\\Metro\\Metro_Data\\Metro_Statistics_OD_20180101_0180107.txt','a') as w:
                w.write(precid+","+pretype+","+pretime+","+presid+","+presname+","+recenttype+","+recenttime+","+recentsid+","+recentsname+"\n")
        precid = recentcid
        pretype = recenttype
        pretime = recenttime
        presid = recentsid
        presname = recentsname
end=time.clock()
print('Running time:',end-start)
'''

#start=time.clock()

def get_Metro_Statistics_OD(filename):
    precid = ''
    pretype = ''
    pretime = ''
    presid = ''
    presname = ''
    f=open('E:\\国土局（2013-2018）\\2017\\{}_sorted.txt'.format(filename),encoding='utf-8')
    w=open('E:\\国土局（2013-2018）\\2017\\Metro_Statistics_OD_{}.txt'.format(filename),'a')
    next(f) #直接跳过第一行
    count=0
    for msg in f:
        count+=1
        if count%500000==0:
            print(count)
        recentcid=msg.split('\t')[0]
        recenttype=msg.split('\t')[1]
        recenttime=msg.split('\t')[2]
        recentsid=msg.split('\t')[4]
        recentsname=msg.split('\t')[5].strip()
        if recentcid==precid and pretype=='21' and recenttype=='22':
            w.write(precid+","+pretype+","+pretime+","+presid+","+presname+","+recenttype+","+recenttime+","+recentsid+","+recentsname+"\n")
        precid = recentcid
        pretype = recenttype
        pretime = recenttime
        presid = recentsid
        presname = recentsname 
    w.close()
    f.close()
    
get_Metro_Statistics_OD('20171002-20171008')

#end=time.clock()
#print('Running time:',end-start)



###############################################################

'''
根据 'Metro_Statistics_OD_' 文件提取出各时间段的出行OD（周期为1小时），并存储至文件 '出行OD_2018-01-{}-{}_2018-01-{}-{}.txt'
'''

df=pd.read_csv('E:\\国土局（2013-2018）\\2018\\Metro_Statistics_OD_20180101_20180107.txt',sep=',',header=None,encoding='gbk',names=['CARDID','TRADETYPE_x','TRADEDATE_x','STATIONID_x','STATIONNAME_x','TRADETYPE_y','TRADEDATE_y','STATIONID_y','STATIONNAME_y'],parse_dates=['TRADEDATE_x'])
df1=df.set_index('TRADEDATE_x')

'''df2=df1['2018-01-01 23:00:00':'2018-01-02 00:00:00']
ser=df2.groupby(['STATIONNAME_x','STATIONNAME_y']).size()
ser.name='出行OD'''

for j in range(1,8):
    for i in range(24):
        print(j,i)
        df2=df1['2018-01-{} {}'.format(str(j).rjust(2,'0'),str(i).rjust(2,'0'))]
        sr=df2.groupby(['STATIONNAME_x','STATIONNAME_y']).size()
        sr.name='出行OD'
        sr.reset_index().to_csv('E:\\Project\\Metro\\Metro_Data\\出行OD_2018-01-{}-{}.txt'.format(str(j).rjust(2,'0'),str(i).rjust(2,'0')), sep='\t', header=True,index=False)
    































