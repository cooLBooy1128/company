import pandas as pd


def mergeID_D(path):
    df=pd.read_csv(path)
    df2=pd.merge(df,df1,left_on='Street_D',right_on='JDName')
    df2.rename(columns={'XZQDM':'StreetID_D'},inplace=True)
    df2[['Time','StreetID_D','Street_D','Cnt']].to_csv(path,encoding='utf-8',index=False)
    
def mergeID_O(path):
    df=pd.read_csv(path)
    df2=pd.merge(df,df1,left_on='Street_O',right_on='JDName')
    df2.rename(columns={'XZQDM':'StreetID_O'},inplace=True)
    df2[['Time','StreetID_O','Street_O','Cnt']].to_csv(path,encoding='utf-8',index=False)

def mergeID_OD(path):
    df=pd.read_csv(path)
    df2=pd.merge(df,df1,left_on='Street_O',right_on='JDName')
    df2.rename(columns={'XZQDM':'StreetID_O'},inplace=True)
    df3=pd.merge(df2,df1,left_on='Street_D',right_on='JDName')
    df3.rename(columns={'XZQDM':'StreetID_D'},inplace=True)
    df3[['Time','StreetID_O','StreetID_D','Street_O','Street_D','Cnt']].to_csv(path,encoding='utf-8',index=False)

df1=pd.read_excel(r'G:\参考资料与工具\深圳街道代码.xlsx')
pathO=r'G:\WebGis平台\data\地铁\Metro_Street_O_20171002-20171008_Hour.txt'
pathD=r'G:\WebGis平台\data\地铁\Metro_Street_D_20171002-20171008_Hour.txt'
pathOD=r'G:\WebGis平台\data\地铁\Metro_Street_OD_20171002-20171008_Hour.txt'
mergeID_O(pathO)
mergeID_D(pathD)
mergeID_OD(pathOD)