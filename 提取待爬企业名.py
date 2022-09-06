#coding=gbk

import pandas as pd

        
if __name__ == '__main__':  
    df1=pd.read_excel(r'C:\Users\szu\Desktop\吉华街道项目\企业\企业数据爬虫\对外投资公司名.xlsx')
    df2=df1.drop_duplicates()
    df3=pd.DataFrame(df2['对外投资公司'])
    df3=df3.rename({'对外投资公司':'cname'},axis=1)
    df3.to_excel(r'C:\Users\szu\Desktop\吉华街道项目\企业\企业数据爬虫\待爬企业名.xlsx',index=False)
    
    

    
    
    
    
    
    
    
    
    
    
    