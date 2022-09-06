from datetime import datetime
import pandas as pd

def duration(s,e):
    s=datetime.strptime(s,'%Y-%m-%d %H:%M:%S')
    e=datetime.strptime(e,'%Y-%m-%d %H:%M:%S')
    return (e-s).total_seconds()
    
w=open(r'G:\联通_手机信令\Phone_CU_Shenzhen_2011\聚合.txt','a',encoding='utf8')
w.write('UID,DATETIME,LON,LAT\n')
count=0
with open(r'G:\联通_手机信令\Phone_CU_Shenzhen_2011\汇总_sorted.txt','r',encoding='utf8') as f:
    next(f)
    preuid='9715'
    pretime='2011-08-01 11:04:30'
    prelon='114.12026000000002'
    prelat='22.54077'   
    for row in f:
        count+=1
        if count%100000==0:
            print(count)
        l=row.split(',')
        #print(l)
        uid=l[0]
        time=l[1]
        lon=l[2]
        lat=l[3] 
        if uid==preuid and duration(pretime,time)<=3600 and lon==prelon and lat==prelat:
            continue
        else:
            #print(preuid,pretime,prelon,prelat)
            w.write(preuid+','+pretime+','+prelon+','+prelat+'\n')
            preuid=uid
            pretime=time
            prelon=lon
            prelat=lat
w.close()
