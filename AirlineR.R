#import packages
install.packages("wordcloud")
install.packages("tidytext")
install.packages("glue")
library(dplyr)
library(ggplot2)
library(tidyverse)
library(tidytext)
library(readr)
library(wordcloud)
library(tidyr)
library(glue)
library(stringr)

#read the file
tweetdb <- read_csv('Tweets.csv', col_types = cols(.default = "c"))
str(tweetdb)

## tokenize words into cleaned data
tidy_tweetdb <- tweetdb %>% 
  group_by(airline) %>% 
  unnest_tokens(word, text) %>% 
  ungroup()

## remove stop words
# pull out stop words from tidytext package
data("stop_words")
# anti_join will remove these stop word lists
tidy_tweetdb <- tidy_tweetdb %>% 
  anti_join(stop_words)

# remove http elements manually
tweetdb$stripped_text <- gsub("http.*","",  tweetdb$text)
tweetdb$stripped_text <- gsub("https.*","", tweetdb$stripped_text)
tweetdb$stripped_text <- gsub("#[a-z,A-Z]*","", tweetdb$stripped_text)
#tweetdb$stripped_text <- gsub("@[a-z,A-Z*","", tweetdb$stripped_text)

# table of the most common words across all airlines
freq <- tidy_tweetdb %>%
  count(word, sort = TRUE)

# visualize with a wordcloud
wordcloud(freq$word, freq$n, min.freq = 45, random.order = FALSE)
warnings()

# visualize most common words across all airlines
tidy_tweetdb %>%
  count(word, sort = TRUE) %>%
  filter(n > 120) %>%
  mutate(word = reorder(word, n)) %>%
  ggplot(aes(word, n)) +
  geom_col() +
  xlab(NULL) +
  coord_flip()

# visualize most common words in each airline
tidy_tweetdb %>%
  group_by(airline) %>% 
  count(word, sort = TRUE) %>% 
  filter(n > 25) %>%
  mutate(word = reorder(word, n)) %>% 
  ungroup() %>% 
  mutate(airlines = reorder(airline, n)) %>% 
  ggplot(aes(word, n)) +
  geom_col() +
  facet_grid(~ airlines) +
  xlab(NULL) +
  coord_flip() +
  theme(axis.text.y = element_text(size = 8))

# get words already in the Bing sentiment dictionary
bingWords <- get_sentiments("bing")[,1]

# get the top 50 most frequent words, excluding stop words
# and word already in the "bing" lexicon
top50Words <- allTokens %>% 
  anti_join(stop_words) %>% # remove stop words
  anti_join(bingWords) %>% # remove words in the bing lexicon
  count(word, sort = T) %>% # sort by frequency
  top_n(50) # get the top 100 terms


