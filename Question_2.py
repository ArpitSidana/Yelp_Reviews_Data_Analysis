import json
import pandas as pd
import json
from pandas import DataFrame
import matplotlib
from matplotlib import pyplot as plt
import numpy as np

data1 = []

with open('business.json') as f1:
    for line in f1:
        data1.append(json.loads(line))
b=DataFrame(data1)

b['categories']=b['categories'].astype(str)
b['categories']=b['categories'].str.replace('[','')
b['categories']=b['categories'].str.replace(']','')
b['categories']=b['categories'].str.replace('"','')
b['categories']=b['categories'].str.replace("'",'')

b.columns = [i.strip() for i in b.columns]
b=b.dropna()

#all fast food chains data
fast_food=b[b['categories'].str.contains('Fast Food')]

#filter the data based on required columns
df = fast_food[['name','state','stars']]

#restaurant count for every state
state_rest = df.groupby(['state', 'name']).count()
#state_rest.reset_index(inplace=True)
rating = df.groupby(['state', 'name']).sum()
state_rest['rating']=rating
state_rest.reset_index(inplace=True)
rest_count_above10 = state_rest[state_rest['stars']>10]

#total restaurants in every state
state_rest_count = DataFrame(df.groupby(['state']).count()['stars'])
state_rest_count.reset_index(inplace=True)

new_df=pd.merge(state_rest,state_rest_count,on='state',how='left')
new_df['presence']=new_df['stars_x']/new_df['stars_y']

#chains with state presence more than 10%
state_pres_10=new_df[new_df['presence']>0.10].sort(ascending=False)
state_pres_10.groupby(['name','state'])

x=state_pres_10.groupby(['name','state']).sum()
#x.reset_index(inplace=True)


McDonalds=x.loc["McDonald's"]
McDonalds.reset_index(inplace=True)
Subway=x.loc["Subway"]
Subway.reset_index(inplace=True)
Tacobell=x.loc["Taco Bell"]
Tacobell.reset_index(inplace=True)

Tacobell.head()
Subway.head()
McDonalds.head()

#Percentage presence of McDonalds out of the total number of fast food joints 
plt.figure(1)
objects = (McDonalds['state'])
y_pos = np.arange(len(objects))
plt.bar(y_pos,McDonalds['presence']*100, align='center', alpha=0.5, color='brown')
plt.xticks(y_pos, objects)
plt.xlabel('State', fontsize=15)
plt.ylabel('Percentage of total number of fast food joints', fontsize=15)
plt.ylim(0,100)
plt.title('Percentage presence of McDonalds out of the total number of fast food joints', fontsize=20)
plt.figure(1).show()

#Percentage presence of Subway out of the total number of fast food joints 
plt.figure(2)
objects = (Subway['state'])
y_pos = np.arange(len(objects))
plt.bar(y_pos,Subway['presence']*100, align='center', alpha=0.5, color='brown')
plt.xticks(y_pos, objects)
plt.xlabel('State', fontsize=15)
plt.ylabel('Percentage of total number of fast food joints', fontsize=15)
plt.ylim(0,100)
plt.title('Percentage presence of Subway out of the total number of fast food joints ', fontsize=20)
plt.figure(2).show()

#Percentage presence of Tacobell out of the total number of fast food joints 
plt.figure(3)
objects = (Tacobell['state'])
y_pos = np.arange(len(objects))
plt.bar(y_pos,Tacobell['presence']*100, align='center', alpha=0.5, color='brown')
plt.xticks(y_pos, objects)
plt.xlabel('State', fontsize=15)
plt.ylabel('Percentage of total number of fast food joints', fontsize=15)
plt.ylim(0,100)
plt.title('Percentage presence of Tacobell out of the total number of fast food joints ', fontsize=20)
plt.figure(3).show()

