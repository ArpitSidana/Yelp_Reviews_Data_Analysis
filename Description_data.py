import json
import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame
import numpy as np

data1=[]
data2=[]
with open('C:/Users/Malavika/OneDrive/MSBA 6310 Python/Data sets/y/y1/Yelp/review.json') as f1:
    for line in f1:
        data1.append(json.loads(line))
df=DataFrame(data1)

#Users over years
df['date']=pd.to_datetime(df['date'],format='%Y-%m-%d')
x=df['user_id'].groupby(df.index).nunique()
x=df['user_id'].groupby(df.index).nunique()
x.plot.bar(color='purple')
plt.ylabel('Number of distinct users',fontsize=15)
plt.xlabel('Years',fontsize=15)
plt.title('Number of users by Year',fontsize=20)


#Users over states
with open('C:/Users/Malavika/OneDrive/MSBA 6310 Python/Data sets/y/y1/Yelp/business.json') as f1:
    for line in f1:
        data2.append(json.loads(line))
df2=DataFrame(data2)

df3=pd.merge(df,df2,on="business_id",how="left")

df3['date']=pd.to_datetime(df3['date'],format='%Y-%m-%d')
x=df3['user_id'].groupby(df3['state']).nunique()
x=df3['user_id'].groupby(df3['state']).nunique()
x=x.sort_values(axis=0, ascending=False)
x.plot(kind='bar',color='green')
plt.ylabel('Number of distinct users',fontsize=15)
plt.xlabel('State',fontsize=15)
plt.title('Number of users by State',fontsize=20)

#category tags

c = 0
data1 = []
with open('business.json') as f1:
    for line in f1:
        if c<=1000:
            data1.append(json.loads(line))
            c+=1

b=DataFrame(data1)
b['categories']=b['categories'].astype(str)
b['categories']=b['categories'].str.replace('[','')
b['categories']=b['categories'].str.replace(']','')
b['categories']=b['categories'].str.replace('"','')
b['categories']=b['categories'].str.replace("'",'')

c1 = list(b['categories'])

# Create list of all words in every row

c2 = []
for i in c1:
    for j in range(len(i.split(','))):
        c2.append(i.split(',')[j])

# Remove u from start of every character        
c3 = []
for i in c2:
    c3.append((''.join(i.split('u', 1))).strip())

c3 = pd.DataFrame(c3, columns=['Category'])
c4 = c3['Category'].value_counts()
c4 = c4[c4>40]

# Plot
c4.plot.bar(color='orange')
plt.title('Count of most popular "Category" tags',fontsize=20)
plt.xlabel("Category Tag",fontsize=15)
plt.ylabel("Number of businesses",fontsize=15)
plt.show()