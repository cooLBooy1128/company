#coding=gbk

import pandas as pd

        
if __name__ == '__main__':  
    df=pd.read_excel(r'C:\Users\szu\Desktop\�����ֵ���Ŀ\��ҵ\��ҵ��������\�����ֵ�����.xlsx')
    df1=pd.read_csv(r'C:\Users\szu\Desktop\�����ֵ���Ŀ\��ҵ\��ҵ��������\�����ֵ�.txt',header=None)
    l=list(df['cname'])
    for i in set(df1[0]):
        #print(i)
        if i in l:
            l.remove(i)
    df2=pd.DataFrame(l,columns=['cname'])
    df2.to_excel(r'C:\Users\szu\Desktop\�����ֵ���Ŀ\��ҵ\��ҵ��������\������ҵ��.xlsx',index=False)
    
    

    
    
    
    
    
    
    
    
    
    
    