#coding=gbk

import pandas as pd

        
if __name__ == '__main__':  
    df1=pd.read_excel(r'C:\Users\szu\Desktop\�����ֵ���Ŀ\��ҵ\��ҵ��������\����Ͷ�ʹ�˾��.xlsx')
    df2=df1.drop_duplicates()
    df3=pd.DataFrame(df2['����Ͷ�ʹ�˾'])
    df3=df3.rename({'����Ͷ�ʹ�˾':'cname'},axis=1)
    df3.to_excel(r'C:\Users\szu\Desktop\�����ֵ���Ŀ\��ҵ\��ҵ��������\������ҵ��.xlsx',index=False)
    
    

    
    
    
    
    
    
    
    
    
    
    