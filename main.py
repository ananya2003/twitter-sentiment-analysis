import tweepy
from textblob import TextBlob
import pandas as pd
import numpy as np
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
plt.style.use("fivethirtyeight")
# twitter api credentials
consumerKey ='pTSCTQbD6uFIwXvJ8UumL4Bv5'
consumerSecret='PFw8HlSuMZjxw97VK4NUemvdSmHNsmaYC17mlKbguXgFtqJvxt'
accessKey='3277465040-fFmBImVNrG8Uol5UBLPFdqIumEDEVOL62F1Pqwg'
accessToken='YjnEbaBqV8Tqs7Zu4BU535sOMkirwqT3vn3FDmH237rjN'

# Create the authentication object
authenticate=tweepy.OAuthHandler(consumerKey,consumerSecret)
# set the access token and access token secret
authenticate.set_access_token(accessKey,accessToken)
# create tha api object while passing the authentication information
api=tweepy.API(authenticate,wait_on_rate_limit="true")
# Extraxt tweet from the twitter user
posts=api.user_timeline(screen_name="NarendraModi", count=100, lang="en", tweet_mode="extended")
tweets=posts[0:20] 
df=pd.DataFrame([tweet1.full_text for tweet1 in tweets], columns=['tweets'])
def cleantext(text):
    text=re.sub(r'@[a-zA-Z0-9]+',"",text)
    text=re.sub(r'#',"",text)
    text=re.sub(r'RT[\s]+',"",text)
    text=re.sub(r'https?:\/\/\S+',"",text)
    return text
df["tweets"]=df["tweets"].apply(cleantext)
# create a function to get subjectivity
def GetSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity
#  craete a function to get polarity
def GetPolarity(text):
    return TextBlob(text).sentiment.polarity
# create the two column
df["subjectivity"]=df["tweets"].apply(GetSubjectivity)
df["polarity"]=df["tweets"].apply(GetPolarity)
# show the new dataframe with the new columns
# plot the word cloud
allwords=" ".join([twts for twts in df["tweets"]])
wordCloud=WordCloud(width=500,height=300,random_state=21,max_font_size=119).generate(allwords)
plt.imshow(wordCloud, interpolation="bicubic")
plt.axis("off")
# plt.show()
def getAnalysis(score):
    if score<0:
        return "Negative"
    elif score==0:
        return "Neutral"
    else:
        return "Positive"
df["analysis"]=df["polarity"].apply(getAnalysis)
# print the positive tweets
j=1
sortedDF=df.sort_values(by=['polarity'])
for i in range(0,sortedDF.shape[0]):
    if (df['analysis'][i]=='Positive'):
        # print (str(j)+')'+ sortedDF["tweets"][i])
        # print()
        j=j+1
# print the negative tweets
j=1
sortedDF1=df.sort_values(by=['polarity'], ascending="False")
# print(df["analysis"])

for i in range(0,sortedDF1.shape[0]):
    if(df['analysis'][i]=='Negative'):
        # print (str(j)+')'+ sortedDF["tweets"][i])
        # print()
        j=j+1
# plot the subjectivity and polarity
plt.figure(figsize=(8,6))
# for i in range(0,df.shape[0]):
    # plt.scatter(df["polarity"][i], df["subjectivity"][i], color="purple")
    # plt.title("first project of DA")
    # plt.xlabel("polarity")
    # plt.ylabel("subjectivity")
# plt.show()
#  show the value counts
df["analysis"].value_counts()
plt.title("fst da")
plt.xlabel("Sentiment")
plt.ylabel("Counts")
df["analysis"].value_counts().plot(kind="bar")
plt.show()


    

