import json
import pandas as pd
from pandas import DataFrame
import numpy as np
import datetime
import forecastio
import statsmodels.formula.api as sm
import matplotlib.pyplot as plt

#forecast io module is installed using pip install python-forecastio

###Reading business and review json files
data1 = []
data2 = []

with open('review.json') as f1:
    for line in f1:
        data1.append(json.loads(line))
review=DataFrame(data1)

with open('business.json') as f1:
    for line in f1:
        data1.append(json.loads(line))
business=DataFrame(data1)

###Code to determine sentiment score for user reviews in the month of January 2015

good=pd.read_csv('good.txt',error_bad_lines=False, squeeze=True)
good=good.tolist()
good=map(str.lower,good)

bad=pd.read_csv('bad.txt',error_bad_lines=False,squeeze=True)
bad=bad.tolist()
bad=map(str.lower,bad)

business['business_id']=business['business_id'].astype(str)

review['date']=pd.to_datetime(review['date'],format='%Y-%m-%d')
review_2015=review[review.date.dt.year == 2015]                                 

review_2015['date']=pd.to_datetime(review_2015['date'],format='%Y-%m-%d')
review_2015_1=review_2015[review_2015.date.dt.month == 1]  #filtering for Jan 2015

review=review_2015_1['text'].str.lower().str.split()
review=review.reset_index(drop=True)

#Counts of good words
counts=list()
for i in range(len(review)):
    count=0
    for word in good:
        if word in map(str.lower,review[i]):
            count+=1
    counts.append(count)

Good=pd.Series(counts)
review_2015_1['Good_cnt']=Good.values

#Counts of bad words
counts_bad=list()
for i in range(len(review)):
    count=0
    for word in bad:
        if word in review[i].lower():
            count+=1
    counts_bad.append(count)

Bad=pd.Series(counts_bad)
review_2015_1['Bad_cnt']=Bad.values

review_2015_1['Total words']=[len(review[i]) for i in range(len(review))]
review_2015_1['Sentiment score']=(review_2015_1['Good_cnt']-review_2015_1['Bad_cnt'])/review_2015_1['Total words']
review_2015_1['Sentiment buckets'] = np.where(review_2015_1['Sentiment score']>0, 'Positive',np.where(review_2015_1['Sentiment score']<0,'Negative', 'Neutral'))
sentiment_2015_1= review_2015_1

###Code for extracting data for unique businesses for user reviews in the month of January 2015.

review_2015_1['date']=pd.to_datetime(review_2015_1['date']) 

#Unique businesses for 2015
businessid=list(review_2015_1['business_id'].unique())
business_2015_1=business[business['business_id'].isin(businessid)]

###Extracting weather data for all unique businesses based on latitude and longitude

api_key = "6015a5512ba5740ade21189d15581793"
def temp(lat,lng):
    attributes = ["temperature"]
    times = []
    data = {}
    for attr in attributes:
        data[attr] = []
        start = datetime.datetime(2015, 1, 1)
    for offset in range(1, 31):
        forecast = forecastio.load_forecast(api_key, lat, lng, time=start+datetime.timedelta(offset), units="us")
        h = forecast.hourly()
        d = h.data
        for p in d:
            times.append(p.time)
            for attr in attributes:
                data[attr].append(p.d[attr])
    df = pd.DataFrame(data, index=times)
    df['date']=df.index.astype('str').str.split(' ').str.get(0)
    avg_temp=DataFrame(df['temperature'].groupby(df['date']).mean())
    avg_temp['latitude']=lat
    avg_temp['longitude']=lng
    return avg_temp

avg_temp=DataFrame()
for i in range(len(business_2015_1)):
    avg_temp= avg_temp.append(temp(business_2015_1['latitude'][i],business_2015_1['longitude'][i]))
weather_final=avg_temp

###Code to get latitude and longitude information from business file, append to each user reviews, to which temperature data is also joined

business_sentiment=pd.merge(sentiment_2015_1,business,on='business_id',how='left')
business_sentiment['user_review_stars']= business_sentiment['stars_x']

#Selecting required columns
business_sentiment=business_sentiment[['business_id','latitude','longitude','date','user_review_stars','user_id','Sentiment score','Sentiment buckets']] #business_sentiment has user reviews with sentiment score, business latitude/longitude for which the review is given

###Regression analysis

business_sentiment['date']=pd.to_datetime(business_sentiment['date'])
weather_final['date']=pd.to_datetime(weather_final['date'])
final_sentiment= pd.merge(business_sentiment, weather_final, on=['date','latitude','longitude'], how='inner')

dummy_stars=DataFrame(pd.get_dummies(final_sentiment['user_review_stars']))
final_sentiment['score']=final_sentiment['Sentiment score']
final_sentiment['star1']=dummy_stars[1]
final_sentiment['star2']=dummy_stars[2]
final_sentiment['star3']=dummy_stars[3]
final_sentiment['star4']=dummy_stars[4]

result = sm.ols(formula='score ~ ' +'temperature + star1+ star2+ star3+ star4', data=final_sentiment).fit()
print result.summary()

###Plotting and visualization
yelp_analysis=final_sentiment[['business_id','date','state','Sentiment score','Sentiment buckets','temperature','temp_bucket','user_review_stars']]

#Temperature vs sentiment score
x=yelp_analysis['temperature']
y=yelp_analysis['Sentiment score']
fig1, ax = plt.subplots()
fit = np.polyfit(x, y, deg=1)
ax.plot(x, fit[0] * x + fit[1], color='red')
ax.scatter(x, y)
plt.title('Temperature vs Sentiment Score',fontsize=20)
plt.xlabel('Temperature in degree Farenheit',fontsize=15)
plt.ylabel('Sentiment Score',fontsize=15)
fig1.show()

#User review stars vs sentiment scores
x=yelp_analysis['user_review_stars']
y=yelp_analysis['Sentiment score']
fig2, ax = plt.subplots()
fit = np.polyfit(x, y, deg=1)
ax.plot(x, fit[0] * x + fit[1], color='red')
ax.scatter(x, y)
plt.title('Stars rating vs Sentiment Score',fontsize=20)
plt.xlabel('Stars rating',fontsize=15)
plt.ylabel('Sentiment Score',fontsize=15)
fig2.show()

#Customer Sentiment vs Stars Rating
df=yelp_analysis.groupby(["stars_x", "Sentiment buckets"]).size().unstack()
df.reset_index(inplace=False)
df.plot.bar(color=['red','yellow','green'],alpha=0.5)
plt.xlabel('Stars Rating',fontsize=15)
plt.title('Customer Sentiment vs Stars Rating',fontsize=20)
plt.ylabel('Number of Comments',fontsize=15)
plt.show()


