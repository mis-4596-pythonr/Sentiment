#!/usr/bin/env python
# coding: utf-8

# In[2]:


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


# In[3]:


#read the data
data = pd.read_csv("~/Desktop/Machine_Learning/Twitter/Tweets.csv")

data.head()


# In[4]:


#read in the columns we need
data = data[['tweet_id','airline_sentiment','airline','text']]

data.head()


# In[5]:


#remove twitter handles and special characters
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


# In[6]:


#tokenize words into cleaned data
import re

def tokenize(text):
    tokens = re.split('\W+', text)
    return tokens

data['tokens'] = data['tidy_tweet'].apply(lambda x: tokenize(x.lower()))

data.head()


# In[7]:


#remove stopwords
import nltk
from nltk.corpus import stopwords
stopword = nltk.corpus.stopwords.words('english')

def remove_stopwords(tokenized_list):
    text = [word for word in tokenized_list if word not in stopword]
    return text

data['words'] = data['tokens'].apply(lambda x: remove_stopwords(x))

data.head()


# In[8]:


#remove punctuation
punct = string.punctuation

def remove_punct(tokenized_list):
    text = [word for word in tokenized_list if word not in punct]
    return text

data['words_no_punct'] = data['words'].apply(lambda x: remove_punct(x))

data.head()


# In[9]:


#remove common words specific to the airline database
airline_stopword = (" ", "http", "co", "united", "american","americanair", "southwest","southwestair", "us airways", "usairways", "delta", "jetblue", "virgin American", "virginamerica", "http", "aa", "4", "3", "2", "1", "t.co")

def remove_airline_stopwords(tokenized_list):
    text = [word for word in tokenized_list if word not in airline_stopword]
    return text

data['words_no_airline'] = data['words_no_punct'].apply(lambda x: remove_airline_stopwords(x))

data.head()


# In[11]:


#visualize the common words in a wordcloud
all_words = ','.join([str(v) for v in data['words_no_airline']])
from wordcloud import WordCloud
wordcloud = WordCloud(width=800, height=500, random_state=21, max_font_size=110).generate(all_words)

plt.figure(figsize=(10, 7))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis('off')
#export the wordcloud
plt.savefig('python_cloud.png')
plt.show()


# In[14]:


#visualize most common words across all airlines
from collections import Counter
all_words = [item
              for sublist in data['words_no_airline']
              for item in sublist]

word_counter = Counter(all_words)
most_common_words = word_counter.most_common()

word_df = pd.DataFrame(most_common_words, columns=['Words','Frequency'])
word_df.head(10)


# In[ ]:


#plot the most common words across all airlines
plt.hist(word_df['Words'])
plt.show(10)


# In[ ]:


#plot most common words by airline
from seaborn import countplot
from matplotlib.pyplot import figure, show
figure()
countplot(data=word_df, y='Words')
show(10)

g = sns.FacetGrid(data=word_df, col='airline')
#sns.set(style="darkgrid")
ax = sns.countplot(x="Words", data=word_df)

