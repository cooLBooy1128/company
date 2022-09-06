import os
import pandas as pd


def all_path(dirname):
    result = []#所有的文件
    for maindir, subdir, file_name_list in os.walk(dirname):
        # print("1:",maindir) #当前主目录
        # print("2:",subdir) #当前主目录下的所有目录
        # print("3:",file_name_list)  #当前主目录下的所有文件
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)#合并成一个完整路径
            ext = os.path.splitext(apath)[1]  # 获取文件后缀,[0]获取的是除文件后缀名以外的内容          
            if ext in filt:
                result.append(apath)
                # print(os.path.splitext(apath)[0],os.path.splitext(apath)[1])
    return result

def get_cnames(result):
    cnames=[]
    for filepath in result:
        #print(get_FileSize(filename))
        size = os.path.getsize(filepath)
        if size < 1024:
            tempfilename = os.path.split(filepath)[1]
            filename = os.path.splitext(tempfilename)[0]
            print(filename)
            cnames.append()
            os.remove(filepath)

def write_cnames(cnames,filename):
    df=pd.DataFrame(cnames,columns=['cname'])
    df.to_excel(filename,index=False)

if __name__=='__main__':
    filt=['.json'] #设置过滤后的文件类型,可以设置多个类型
    result=all_path(r'G:\企业信息\企业基本信息')
    cnames=get_cnames(result)
    write_cnames(cnames,r'G:\企业信息\企业基本信息\小文件企业名.xlsx')