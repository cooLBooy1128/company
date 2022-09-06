import pandas as pd

#读取文件，read_csv()用于读取txt、csv等文本文件；r'G:\项目\深大土木学院项目\深大_20200107\OD\OD_扩样后.txt'为文件路径，根据文件所在位置自行修改；'utf8'为文件编码
df=pd.read_csv(r'G:\项目\深大土木学院项目\深大_20200107\OD\OD_扩样后.txt',encoding='utf8')
#groupby()根据'grid_id_o'字段分组，并在分组后的数据上对‘pop’字段求和
df1=df.groupby('grid_id_o')['pop'].sum().reset_index()
#将df1导入文件r'G:\项目\深大土木学院项目\深大_20200107\OD\O_扩样后.txt'中，文件路径可自行修改
df1.to_csv(r'G:\项目\深大土木学院项目\深大_20200107\OD\O_扩样后.txt',encoding='utf8',index=False)

#groupby()根据'grid_id_d'字段分组，并在分组后的数据上对‘pop’字段求和
df2=df.groupby('grid_id_d')['pop'].sum().reset_index()
#将df2导入文件r'G:\项目\深大土木学院项目\深大_20200107\OD\D_扩样后.txt'中，文件路径可自行修改
df2.to_csv(r'G:\项目\深大土木学院项目\深大_20200107\OD\D_扩样后.txt',encoding='utf8',index=False)