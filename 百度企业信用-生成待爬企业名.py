#coding=gbk

import pandas as pd

        
if __name__ == '__main__':  
    df=pd.read_excel(r'C:\Users\szu\Desktop\吉华街道项目\企业\企业数据爬虫\吉华街道爬虫.xlsx')
    df1=pd.read_csv(r'C:\Users\szu\Desktop\吉华街道项目\企业\企业数据爬虫\吉华街道.txt',header=None)
    l=list(df['cname'])
    for i in set(df1[0]):
        #print(i)
        if i in l:
            l.remove(i)
    df2=pd.DataFrame(l,columns=['cname'])
    df2.to_excel(r'C:\Users\szu\Desktop\吉华街道项目\企业\企业数据爬虫\待爬企业名.xlsx',index=False)
    
    

    
    
    
    
    
    
    
    
    
    
    