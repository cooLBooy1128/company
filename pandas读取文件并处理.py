import pandas as pd

#��ȡ�ļ���read_csv()���ڶ�ȡtxt��csv���ı��ļ���r'G:\��Ŀ\�����ľѧԺ��Ŀ\���_20200107\OD\OD_������.txt'Ϊ�ļ�·���������ļ�����λ�������޸ģ�'utf8'Ϊ�ļ�����
df=pd.read_csv(r'G:\��Ŀ\�����ľѧԺ��Ŀ\���_20200107\OD\OD_������.txt',encoding='utf8')
#groupby()����'grid_id_o'�ֶη��飬���ڷ����������϶ԡ�pop���ֶ����
df1=df.groupby('grid_id_o')['pop'].sum().reset_index()
#��df1�����ļ�r'G:\��Ŀ\�����ľѧԺ��Ŀ\���_20200107\OD\O_������.txt'�У��ļ�·���������޸�
df1.to_csv(r'G:\��Ŀ\�����ľѧԺ��Ŀ\���_20200107\OD\O_������.txt',encoding='utf8',index=False)

#groupby()����'grid_id_d'�ֶη��飬���ڷ����������϶ԡ�pop���ֶ����
df2=df.groupby('grid_id_d')['pop'].sum().reset_index()
#��df2�����ļ�r'G:\��Ŀ\�����ľѧԺ��Ŀ\���_20200107\OD\D_������.txt'�У��ļ�·���������޸�
df2.to_csv(r'G:\��Ŀ\�����ľѧԺ��Ŀ\���_20200107\OD\D_������.txt',encoding='utf8',index=False)