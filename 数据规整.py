import pandas as pd
import os

'''
遍历文件夹'G:\地铁_国土局（2013-2018）\data'下所有目标文件，并将路径存入list
'''
result=[]
for maindir,subdir,filenamelist in os.walk(r'G:\地铁_国土局（2013-2018）\data'):
    #print(maindir,subdir,filenamelist)
    for filename in filenamelist:
        path=os.path.join(maindir,filename)
        if 'Metro_Statistics_OD' in path:
            #print(path)
            result.append(path)

'''
对所有目标文件进行数据规整并保存为原路径
'''
for path in result:
    print(path)
    df=pd.read_csv(path,encoding='gbk',header=None)
    df.dropna(inplace=True)
    df[2]=df[2].astype('datetime64')
    df[6]=df[6].astype('datetime64')
    df[4]=df[4].map(lambda x:x+'站')
    df[8]=df[8].map(lambda x:x+'站')
    df.replace({'草铺站':'草埔站','湾夏站':'湾厦站','深圳北站站':'深圳北站'},inplace=True)
    df.to_csv(path,encoding='utf8',index=False)
    print(path)