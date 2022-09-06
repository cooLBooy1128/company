import pandas as pd
import os

'''
�����ļ���'G:\����_�����֣�2013-2018��\data'������Ŀ���ļ�������·������list
'''
result=[]
for maindir,subdir,filenamelist in os.walk(r'G:\����_�����֣�2013-2018��\data'):
    #print(maindir,subdir,filenamelist)
    for filename in filenamelist:
        path=os.path.join(maindir,filename)
        if 'Metro_Statistics_OD' in path:
            #print(path)
            result.append(path)

'''
������Ŀ���ļ��������ݹ���������Ϊԭ·��
'''
for path in result:
    print(path)
    df=pd.read_csv(path,encoding='gbk',header=None)
    df.dropna(inplace=True)
    df[2]=df[2].astype('datetime64')
    df[6]=df[6].astype('datetime64')
    df[4]=df[4].map(lambda x:x+'վ')
    df[8]=df[8].map(lambda x:x+'վ')
    df.replace({'����վ':'����վ','����վ':'����վ','���ڱ�վվ':'���ڱ�վ'},inplace=True)
    df.to_csv(path,encoding='utf8',index=False)
    print(path)