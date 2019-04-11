#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns
import string
import nltk
import warnings 
warnings.filterwarnings("ignore", category=DeprecationWarning)

get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


#read the data
data = pd.read_csv("~/Desktop/Machine_Learning/Twitter/Tweets.csv")

data.head()


# In[3]:


data = data[['tweet_id','airline_sentiment','airline','text']]

data.head()


# In[4]:


def remove_pattern(input_txt, pattern):
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, '', input_txt)
        
    return input_txt    

# remove twitter handles (@user)
data['tidy_tweet'] = np.vectorize(remove_pattern)(data['text'], "@[\w]*")

# remove special characters, numbers, punctuations
data['tidy_tweet'] = data['tidy_tweet'].str.replace("[^a-zA-Z#]", " ")

data.head()


# In[5]:


#tokenize words into cleaned data
import re

def tokenize(text):
    tokens = re.split('\W+', text)
    return tokens

data['tokens'] = data['tidy_tweet'].apply(lambda x: tokenize(x.lower()))

data.head()


# In[8]:


#remove stopwords
import nltk
from nltk.corpus import stopwords
stopword = nltk.corpus.stopwords.words('english')

def remove_stopwords(tokenized_list):
    text = [word for word in tokenized_list if word not in stopword]
    return text

data['words'] = data['tokens'].apply(lambda x: remove_stopwords(x))

data.head()


# In[9]:


#wordcloud visual
all_words = ','.join([str(v) for v in data['words']])
from wordcloud import WordCloud
wordcloud = WordCloud(width=800, height=500, random_state=21, max_font_size=110).generate(all_words)

plt.figure(figsize=(10, 7))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis('off')
plt.show()


# In[11]:


# function to collect hashtags
def freq(x):
    words = []
    # Loop over the words in the tweet
    for i in x:
        wd = re.findall('(\w+)', text)
        words.append(wd)

    return words


# extracting hashtags from non racist/sexist tweets
wd_positive = freq(data['words'][data['airline_sentiment'] == 'positive'])
# extracting hashtags from racist/sexist tweets
wd_negative = freq(data['words'][data['airline_sentiment'] == 'negative'])
# unnesting list
wd_regular = sum(wd_regular,[])
wd_negative = sum(wd_negative,[])


#plot
a = nltk.FreqDist(wd_regular)
d = pd.DataFrame({'words': list(a.keys()),
                  'Count': list(a.values())})
# selecting top 10 most frequent hashtags     
d = d.nlargest(columns="Count", n = 10) 
plt.figure(figsize=(16,5))
ax = sns.barplot(data=d, x= "word", y = "Count")
ax.set(ylabel = 'Count')
plt.show()


# In[ ]:





# In[ ]:





# In[ ]:




