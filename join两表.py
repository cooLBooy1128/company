import pandas as pd

dfa=pd.read_csv(r'G:\项目\西安大悦城平台\西安各街道网格.txt')
l=dfa[['geohash_id','县','乡']].values
hashmap={}
for i in l:
    hashmap[i[0]]=list(i[1:])
try:
    w=open(r'G:\项目\西安大悦城平台\c1_03_01.txt','a',encoding='utf8')
    w.write('start_grid_id,start_city,end_grid_id,report_month,start_type,end_type,gender,age,pop,start_street,start_district,end_street,end_district\n')
    count=0
    with open(r'G:\项目\西安大悦城平台\西安大悦城_201911\西安大悦城_201911\c1_03_01.txt','r',encoding='utf8') as f:
        for row in f:
            count+=1
            if count%500000==0:
                print(count)
            l=row.split('|')
            start_grid_id=l[0]
            start_city=l[1]
            end_grid_id=l[2]
            report_month=l[3]
            start_type=l[4]
            end_type=l[5]
            gender=l[6]
            age=l[7]
            pop=l[8].strip()
            if hashmap.get(start_grid_id):
                start_district,start_street=hashmap[start_grid_id]
            else:
                start_district,start_street='',''
            if hashmap.get(end_grid_id):
                end_district,end_street=hashmap[end_grid_id]
            else:
                end_district,end_street='',''
            w.write(start_grid_id+','+start_city+','+end_grid_id+','+report_month+','+start_type+','+end_type+','+gender+','+age+','+pop+','+start_street+','+start_district+','+end_street+','+end_district+'\n')
except Exception as e:
    print(e)
finally:
    w.close()


