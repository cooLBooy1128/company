import pandas as pd 


'''
统计出租车出行OD，时间精度：1h，街道尺度
'''
def resampler_OD(df):
    return df.groupby(['XZQMC_x','XZQMC_y']).size()
    
dfa=pd.read_excel(r'G:\WebGis平台\参考资料\自定_深圳地理网格编号.xlsx',sheet_name='深圳市')
df1=pd.read_csv(r'G:\出租车\Fee_FCD_OD_201704\FCD_OD_201704.csv',header=None,encoding='utf8')
df1[1]=pd.to_datetime(df1[1],unit='s',origin=pd.Timestamp('1970-01-01 08:00:00'))
df1[2]=pd.to_datetime(df1[2],unit='s',origin=pd.Timestamp('1970-01-01 08:00:00'))
df1['Gid_O']=df1.apply(lambda x: int(x[3] / 0.0025) * 1000000 + int(x[4] / 0.0025), axis=1)
df1['Gid_D']=df1.apply(lambda x: int(x[5] / 0.0025) * 1000000 + int(x[6] / 0.0025), axis=1)
df2=pd.merge(df1,dfa,left_on='Gid_O',right_on='GID')
df3=pd.merge(df2,dfa,left_on='Gid_D',right_on='GID',how='inner')
df3.drop(columns=['GID_x','GID_y','Id_x','Id_y'],inplace=True)
df4=df3.resample('H',on=1,closed='left',label='left').apply(resampler_OD).reset_index()
df4.rename(columns={1:'Time','XZQMC_x':'Street_O','XZQMC_y':'Street_D',0:'Cnt'},inplace=True)
df4.to_csv(r'G:\WebGis平台\data\出租车\FCD_Street_OD_20170401-20170427_Hour.txt',index=False,encoding='utf8')


'''
统计出租车出行发生量和吸引量，时间精度：1h，街道尺度
'''

'''
直接依据原文件统计发生量，与统计吸引量类似
def resampler_O(df):
    return df.groupby('XZQMC_x').size()
df5=df3.resample('H',closed='left',label='left',on=1).apply(resampler_O).reset_index()
df5.rename(columns={1:'Time','XZQMC_x':'Street_O',0:'Cnt'},inplace=True)
df5.to_csv(r'G:\WebGis平台\data\出租车\FCD_Street_O_20170401-20170427_Hour.txt',index=False,encoding='utf8')
'''

df5=df4.groupby(['Time','Street_O'])['Cnt'].sum().reset_index()
df5.to_csv(r'G:\WebGis平台\data\出租车\FCD_Street_O_20170401-20170427_Hour.txt',index=False,encoding='utf8')

def resampler_D(df):
    return df.groupby('XZQMC_y').size()
df6=df3.resample('H',closed='left',label='left',on=2).apply(resampler_D).reset_index()
df6.rename(columns={2:'Time','XZQMC_y':'Street_D',0:'Cnt'},inplace=True)
df6.to_csv(r'G:\WebGis平台\data\出租车\FCD_Street_D_20170401-20170427_Hour.txt',index=False,encoding='utf8')