import json
import pandas as pd
import numpy as np
from pandas import DataFrame
import plotly.plotly as py

 #Business (b) has only business_id
 #User (u) has only user_id
 #Review (r) has both business_id and user_id

#####################    Business    #########################################

count1=0
business = []
with open('business.json') as f1:
    for line in f1:
        #if count1<=100000:
            business.append(json.loads(line))
            #count1 +=1
b=DataFrame(business)
b=b[['business_id','state']]

##########################    user    #########################################

user = []
count2=0
with open('user.json') as f1:
    for line in f1:
        #if count2<=100000:
            user.append(json.loads(line))
            #count2 +=1
u=DataFrame(user)
u = u[['user_id','review_count','yelping_since']]
u['yelping_since_year'] = u['yelping_since'].apply(lambda x: pd.Series(x.split("-")[0]))
u['yelping_since_year'] = u['yelping_since_year'].astype('int')

u['active']=np.where((u['review_count']>=6)&(u['yelping_since_year']<=2014),1,0)
u['inactive']=np.where((u['active']==1),0,1)

####################    Reference Only     ####################################
u['yelping_since_year'].value_counts().sort_index()
 Users who have been active on yelp (yelping_since) since atleast 2014 or earlier
 are deemed to be significant for our analysis.
###############################################################################

####################    Reference Only     ####################################
u['review_count'].describe(percentiles=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9])
 For significance, we take users with review_count >= (50th percentile) = 6
###############################################################################

######################    review    ###########################################

review = []
count3=0
with open('review.json') as f1:
    for line in f1:
        #if count3<=100000:
            review.append(json.loads(line))
            #count3 +=1
r=DataFrame(review)
r = r[['business_id','user_id']]

######################    merges    ###########################################

 Mapping user_id to business_id
m1 = pd.merge(u,r)
m1 = m1[['business_id','user_id','active','inactive']]

 Mapping business_id to state
m2 = pd.merge(m1, b)
m2 = m2[['active','inactive','state']]

m3 = m2.pivot_table(['active','inactive'], index='state', aggfunc=('sum')) 
m3['active_percentage'] = m3['active']*100/(m3['active']+m3['inactive'])

########################  plot     ############################################

m3 = m3[['active_percentage']]

scl = [[0.0, 'rgb(242,240,247)'],[0.2, 'rgb(218,218,235)'],[0.4, 'rgb(188,189,220)'],\
            [0.6, 'rgb(158,154,200)'],[0.8, 'rgb(117,107,177)'],[1.0, 'rgb(84,39,143)']]

data = [ dict(
        type='choropleth',
        colorscale = scl,
        autocolorscale = False,
        locations = m3.index,                     
        z = m3['active_percentage'].astype(float),
        locationmode = 'USA-states',
        marker = dict(
            line = dict (
                color = 'rgb(255,255,255)',
                width = 2
            ) ),
        colorbar = dict(
            title = "Average Active Users (Percentage(%)) by State")
        ) ]

layout = dict(
        title = 'Average Active Users (Percentage(%)) by State',
        geo = dict(
            scope='usa',
            projection=dict( type='albers usa' ),
            showlakes = True,
            lakecolor = 'rgb(255, 255, 255)'),
             )
    
fig = dict( data=data, layout=layout )
py.iplot( fig, filename='choropleth_active_percentage_per_state' ) 