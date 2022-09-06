import pandas as pd
'''
分文件存储
'''
df=pd.read_csv(r'E:\Project\Metro\Metro_Data\20180101-20180107_sorted.txt',sep='\t',parse_dates=['TRADEDATE'])
df1=df.set_index('TRADEDATE')

for j in range(1,8):
    for i in range(24):
        print(j,i)
        df2=df1['2018-01-{} {}'.format(str(j).rjust(2,'0'),str(i).rjust(2,'0'))]
        sr=df2.groupby(['STATIONNAME','TRADETYPE']).size().unstack()
        sr.to_csv('E:\\Project\\Metro\\Metro_Data\\进出站量_2018-01-{}-{}.txt'.format(str(j).rjust(2,'0'),str(i).rjust(2,'0')), sep='\t', header=True)
   
##################################################

import pandas as pd
'''
整体存储
'''
df=pd.read_csv(r'E:\Project\Metro\Metro_Data\20180101-20180107_sorted.txt',sep='\t',parse_dates=['TRADEDATE'])
df['DAY']=df.TRADEDATE.dt.day
df['HOUR']=df.TRADEDATE.dt.hour
ser=df.groupby(['DAY','HOUR','STATIONNAME','TRADETYPE']).size().unstack(fill_value=0)
ser.to_csv('E:\\Project\\Metro\\Metro_Data\\进出站量_20180101-20180107.txt', sep='\t', header=True)

##################################################

'''
直接读取文件，整体存储
'''
reader=open(r'E:\Project\Metro\Metro_Data\20180101-20180107_sorted.txt',encoding='utf-8')
count=0
dic={}
next(reader)
try:
    for msg in reader:
        count+=1
        if count%200000==0:
            print(count)
        '''if count>100:
            break'''
        recenttype=msg.split('\t')[1]
        recenttime=msg.split('\t')[2]
        recentday=recenttime.split()[0].split('/')[-1]
        if len(recenttime.split())==1:
            recenthour='0'
        else:
            recenthour=recenttime.split()[1].split(':')[0]
        recentsid=msg.split('\t')[4]
        recentsname=msg.split('\t')[5].strip()
        #print(recentday+","+recenthour+","+recentsname+","+recenttype+"\n")
        if (recentday,recenthour,recentsname) not in dic:
            dic[(recentday,recenthour,recentsname)]=[0,0]
        if recenttype=='21':
            dic[(recentday,recenthour,recentsname)][0]+=1
        elif recenttype=='22':
            dic[(recentday,recenthour,recentsname)][1]+=1
except IndexError:
    print(str(count)+","+recenttime+","+recentday+","+recenthour+","+recentsname+","+recenttype+"\n")
reader.close()

writer=open(r'E:\Project\Metro\Metro_Data\进出站量_20180101-20180107.txt','a') 
count=0   
for key in dic:
    count+=1
    if count%100000==0:
        print(count)
    #print(list(key)+dic[key])
    writer.write('\t'.join(list(key)+list(map(str,dic[key])))+'\n')
writer.close()