import pandas as pd 


'''
统计手机信令出行OD，时间精度：1h，街道尺度
'''
dfa=pd.read_excel(r'G:\WebGis平台\参考资料\联通ss2_深圳各街道网格.xlsx',sheet_name='500')
dfr=pd.DataFrame()
for j in range(2,9):
    print('第',j,'个')
    df=pd.read_csv(r'G:\联通_手机信令\联通_广东4市\联通数据广东4市原始\guangdong4citys_201710_od_1_15\ss2_grid_city_od_day_index_201710{}.csv'.format(str(j).rjust(2,'0')),header=None)
    df1=pd.merge(df,dfa,left_on=1,right_on='field_2')
    df2=pd.merge(df1,dfa,left_on=2,right_on='field_2')
    df2.drop(columns=['field_2_y','field_3_y','field_2_x','field_3_x'],inplace=True)
    df3=df2[df2[3]==2]
    for i in range(24):
        print(i)
        df4=df3.groupby(['XZQMC_x','XZQMC_y'])[i+15].sum().reset_index()
        df4.rename(columns={'XZQMC_x':'Street_O','XZQMC_y':'Street_D',i+15:'Cnt'},inplace=True)
        df4['Time']='2017-10-02 {}:00:00'.format(str(j).rjust(2,'0'),str(i).rjust(2,'0'))
        dfr=pd.concat([dfr,df4],ignore_index=True)
        print(i)
dfr['Cnt']=dfr['Cnt'].astype('int')
dfr=dfr[['Time','Street_O','Street_D','Cnt']]
dfr.to_csv(r'G:\WebGis平台\data\手机信令\Phone_Street_OD_20171002-20171008_Hour.txt',index=False,encoding='utf8')


'''
统计手机信令出行发生量和吸引量，时间精度：1h，街道尺度
'''
df5=dfr.groupby(['Time','Street_O'])['Cnt'].sum().reset_index()
df5.to_csv(r'G:\WebGis平台\data\手机信令\Phone_Street_O_20171002-20171008_Hour.txt',index=False,encoding='utf8')

df6=dfr.groupby(['Time','Street_D'])['Cnt'].sum().reset_index()
df6.to_csv(r'G:\WebGis平台\data\手机信令\Phone_Street_D_20171002-20171008_Hour.txt',index=False,encoding='utf8')
