import pandas as pd 


'''
统计地铁出行OD，时间精度：1h，街道尺度
'''
def resampler_OD(df):
    return df.groupby(['XZQMC_x','XZQMC_y']).size()

df=pd.read_excel(r'G:\WebGis平台\参考资料\深圳各街道地铁站.xlsx')
dfa=pd.read_csv(r'G:\地铁_国土局（2013-2018）\data\2017\Metro_Statistics_OD_20171002-20171008.txt',parse_dates=['2','6'])
df1=pd.merge(dfa,df,left_on='4',right_on='Name')
df2=pd.merge(df1,df,left_on='8',right_on='Name')
df2.drop(['Name_x','Name_y'],axis=1,inplace=True)
df3=df2.set_index('2')
df4=df3.resample('H',closed='left',label='left').apply(resampler_OD).reset_index()
df4.rename(columns={'2':'Time','XZQMC_x':'Street_O','XZQMC_y':'Street_D',0:'Cnt'},inplace=True)
df4.to_csv(r'G:\WebGis平台\data\地铁\Metro_Street_OD_20171002-20171008_Hour.txt',index=False,encoding='utf8')


'''
统计地铁出行发生量和吸引量，时间精度：1h，街道尺度
'''

'''
直接依据原文件统计发生量，与统计吸引量类似
def resampler_O(df):
    return df.groupby('XZQMC_x').size()
df5=df2.resample('H',closed='left',label='left',on='2').apply(resampler_O).reset_index()
df5.rename(columns={'2':'Time','XZQMC_x':'Street_O',0:'Cnt'},inplace=True)
df5.to_csv(r'G:\WebGis平台\data\地铁\Metro_Street_O_20171002-20171008_Hour.txt',index=False,encoding='utf8')
'''

df5=df4.groupby(['Time','Street_O'])['Cnt'].sum().reset_index()
df5.to_csv(r'G:\WebGis平台\data\地铁\Metro_Street_O_20171002-20171008_Hour.txt',index=False,encoding='utf8')

def resampler_D(df):
    return df.groupby('XZQMC_y').size()
df6=df2.resample('H',closed='left',label='left',on='6').apply(resampler_D).reset_index()
df6.rename(columns={'6':'Time','XZQMC_y':'Street_D',0:'Cnt'},inplace=True)
df6.to_csv(r'G:\WebGis平台\data\地铁\Metro_Street_D_20171002-20171008_Hour.txt',index=False,encoding='utf8')
