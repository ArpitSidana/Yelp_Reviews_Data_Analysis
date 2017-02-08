import json
import pandas as pd
from pandas import DataFrame, Series
import matplotlib.pyplot as plt

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
c4.plot.bar()
plt.title('Count of most popular "Category" tags')
plt.grid(True)
plt.show()