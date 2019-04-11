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
data("stop_words")
airline_stop_words <- data.frame(word = c("united", "american","americanair", "southwest","southwestair", "us airways", "usairways", "delta", "jetblue", "virgin American", "virginamerica", "http", "aa", "4", "3", "2", "1", "t.co"))
tidy_tweetdb <- tidy_tweetdb %>% 
  anti_join(stop_words) %>% 
  anti_join(airline_stop_words)

# remove http elements manually
tweetdb$stripped_text <- gsub("http.*","",  tweetdb$text)
tweetdb$stripped_text <- gsub("https.*","", tweetdb$stripped_text)
tweetdb$stripped_text <- gsub("#[a-z,A-Z]*","", tweetdb$stripped_text)
tweetdb$stripped_text <- gsub("@[a-z,A-Z*","", tweetdb$stripped_text)

# table of the most common words across all airlines
freq <- tidy_tweetdb %>%
  count(word, sort = TRUE)

# visualize with a wordcloud
wordcloud(freq$word, freq$n, min.freq = 45, random.order = FALSE)

# visualize most common words across all airlines
tidy_tweetdb %>%
  count(word, sort = TRUE) %>%
  filter(n > 500) %>%
  mutate(word = reorder(word, n)) %>%
  ggplot(aes(word, n)) +
  geom_col() +
  xlab(NULL) +
  coord_flip()

#positive and negative words
tidy_tweetdb %>%
  group_by(airline_sentiment) %>%
  count(word, sort = TRUE) %>% 
  filter(n>200) %>%
  ungroup() %>%
  mutate(word = reorder(word, n)) %>%
  ggplot(aes(word, n, fill = airline_sentiment)) +
  geom_col(show.legend = FALSE) +
  #facet_wrap(~airline_sentiment, scales = "free_y") #+
  #labs(title = "Sentiment during the 2013 flood event.",
  #y = "Contribution to sentiment",
  #x = NULL) +
  coord_flip()


# visualize most common words in each airline
tidy_tweetdb %>%
  group_by(airline) %>% 
  count(word, sort = TRUE) %>% 
  filter(n > 100) %>%
  mutate(word = reorder(word, n)) %>% 
  ungroup() %>% 
  mutate(airlines = reorder(airline, n)) %>% 
  ggplot(aes(word, n)) +
  geom_col() +
  facet_grid(~ airlines) +
  xlab(NULL) +
  coord_flip() +
  theme(axis.text.y = element_text(size = 8)) +
  labs(title="Word Frequency by Airline", xlab="Word Frequency", ylab="Tweet")

