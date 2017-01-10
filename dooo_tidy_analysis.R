library(dplyr)
library(tidytext)
library(stringr)
library(ggplot2)
library(tidyr)
library(tibble)
library(scales)
library(reshape2)
library(wordcloud)
library(lubridate)
library(tm)
library(topicmodels)

# import and tidy scraped text, fix dates to be real dates
# tokenize by word

dooo_texts <- read.csv('dooo_all_data_Jan6_clean.csv')

dooo_tidy <- as_tibble(dooo_texts) %>%
  transmute(author,
            title,
            url,
            date = as.Date(as.character(strptime(dooo_texts$date, '%m/%d/%Y'))),
            text = as.character(text)) %>%
  unnest_tokens(word, text)

dooo_no_stop <- dooo_tidy %>%
  anti_join(stop_words)

# find most common non-stop words and plot

dooo_no_stop %>%
  count(word, sort=TRUE) %>%
  filter(n > 300) %>%
  mutate(word = reorder(word, n)) %>%
  ggplot(aes(word, n)) +
  geom_bar(stat = 'identity') +
  xlab(NULL) +
  ylab('Word count') +
  coord_flip()

# find most common non-stop words and plot: Tim & Jim only

dooo_no_stop %>%
  filter(author %in% c('Tim Owens', 'Jim Groom')) %>%
  count(word, sort=TRUE) %>%
  filter(n > 200) %>%
  mutate(word = reorder(word, n)) %>%
  ggplot(aes(word, n)) +
  geom_bar(stat = 'identity') +
  xlab('NULL') +
  ylab('Word count') +
  coord_flip()

# find most common non-stop words and plot: no Tim & Jim

dooo_no_stop %>%
  filter(!author %in% c('Tim Owens', 'Jim Groom')) %>%
  count(word, sort=TRUE) %>%
  filter(n > 70) %>%
  mutate(word = reorder(word, n)) %>%
  ggplot(aes(word, n)) +
  geom_bar(stat = 'identity') +
  xlab(NULL) +
  ylab('Word count') +
  coord_flip()

# find most common non-stop words and plot: Jim only

dooo_no_stop %>%
  filter(author == 'Jim Groom') %>%
  count(word, sort=TRUE) %>%
  filter(n > 200) %>%
  mutate(word = reorder(word, n)) %>%
  ggplot(aes(word, n)) +
  geom_bar(stat = 'identity') +
  xlab(NULL) +
  ylab('Word count') +
  coord_flip()

# find most common non-stop words and plot: no Jim

dooo_no_stop %>%
  filter(!author == 'Jim Groom') %>%
  count(word, sort=TRUE) %>%
  filter(n > 85) %>%
  mutate(word = reorder(word, n)) %>%
  ggplot(aes(word, n)) +
  geom_bar(stat = 'identity') +
  xlab(NULL) +
  ylab('Word count') +
  coord_flip()

# find most prolific authors (by word, including stop words) and plot

dooo_tidy %>%
  count(author, sort=TRUE) %>%
  filter(n > 500, n < 50000, author != 'none') %>%
  mutate(author = reorder(author, n)) %>%
  ggplot(aes(author, n)) +
  geom_bar(stat = 'identity') +
  xlab('Author') +
  ylab('Word count') +
  coord_flip()

# just how much has Jim written?!

dooo_tidy %>%
  count(author == 'Jim Groom')
length(dooo_tidy[dooo_tidy$author=='Jim Groom',]$word)/
  length(dooo_tidy$word)

# only jim

jim <- dooo_no_stop %>%
  filter(author == 'Jim Groom')

# no jim or tim

nojim <- dooo_no_stop %>%
  filter(author != 'Jim Groom')

# only UMW

umw_authors <- c('Jim Groom',
                 'Tim Owens',
                 'Martha Burtis',
                 'Jesse Stommel',
                 'Kris Shaffer',
                 'Parrish Waters',
                 'Debra Schleef',
                 'Lee Skallerup Bessette',
                 'Richard V. Hurley',
                 'Zach Whalen',
                 'Gardner Campbell',
                 'Laura Moyer',
                 'Brynn Boyer')
umw_corpus <- dooo_no_stop %>%
  filter(author %in% umw_authors)

# no UMW

no_umw <- dooo_no_stop %>%
  filter(!author %in% umw_authors)

# compare word frequency (UMW v. rest of corpus)

umw_percent <- umw_corpus %>%
  count(word) %>%
  transmute(word, umwfreq = n / sum(n))

frequency <- no_umw %>%
  count(word) %>%
  mutate(other = n / sum(n)) %>%
  left_join(umw_percent) %>%
  ungroup()

ggplot(frequency, aes(x = other, y = umwfreq, color = abs(umwfreq - other))) +
  geom_abline(color = "gray40", lty = 2) +
  geom_jitter(alpha = 0.1, size = 2.5, width = 0.3, height = 0.3) +
  geom_text(aes(label = word), check_overlap = TRUE, vjust = 1.5) +
  scale_x_log10(labels = percent_format()) +
  scale_y_log10(labels = percent_format()) +
  scale_color_gradient(limits = c(0, 0.001), low = "darkslategray4", high = "gray75") +
  theme(legend.position="none") +
  labs(y = 'UMW Faculty/Staff', x = 'Everyone else')

# compare word frequency (Jim v. rest of corpus)

jim_percent <- jim %>%
  count(word) %>%
  transmute(word, jimfreq = n / sum(n))

frequency <- nojim %>%
  count(word) %>%
  mutate(other = n / sum(n)) %>%
  left_join(jim_percent) %>%
  ungroup()

ggplot(frequency, aes(x = other, y = jimfreq, color = abs(jimfreq - other))) +
  geom_abline(color = "gray40", lty = 2) +
  geom_jitter(alpha = 0.1, size = 2.5, width = 0.3, height = 0.3) +
  geom_text(aes(label = word), check_overlap = TRUE, vjust = 1.5) +
  scale_x_log10(labels = percent_format()) +
  scale_y_log10(labels = percent_format()) +
  scale_color_gradient(limits = c(0, 0.001), low = "darkslategray4", high = "gray75") +
  theme(legend.position="none") +
  labs(y = 'Jim Groom', x = 'Everyone else')

# only jim and tim

jimtim <- dooo_no_stop %>%
  filter(author %in% c('Tim Owens', 'Jim Groom'))

# no jim or tim

nojimtim <- dooo_no_stop %>%
  filter(!author %in% c('Tim Owens', 'Jim Groom'))

# compare word frequency (Jim/Tim v. rest of corpus)

jimtim_percent <- jimtim %>%
  count(word) %>%
  transmute(word, jimtimfreq = n / sum(n))

frequency <- nojimtim %>%
  count(word) %>%
  mutate(other = n / sum(n)) %>%
  left_join(jimtim_percent) %>%
  ungroup()

ggplot(frequency, aes(x = other, y = jimtimfreq, color = abs(jimtimfreq - other))) +
  geom_abline(color = "gray40", lty = 2) +
  geom_jitter(alpha = 0.1, size = 2.5, width = 0.3, height = 0.3) +
  geom_text(aes(label = word), check_overlap = TRUE, vjust = 1.5) +
  scale_x_log10(labels = percent_format()) +
  scale_y_log10(labels = percent_format()) +
  scale_color_gradient(limits = c(0, 0.001), low = "darkslategray4", high = "gray75") +
  theme(legend.position="none") +
  labs(y = 'Jim & Tim', x = 'Everyone else')

# Who writes about Virginia Woolf?

dooo_tidy %>%
  filter(word == 'woolf') %>%
  count(title, sort=TRUE)

# sentiment analysis by article

article_sentiment <- dooo_no_stop %>%
  inner_join(get_sentiments("bing")) %>%
  count(title, sentiment) %>%
  spread(sentiment, n, fill = 0) %>%
  mutate(sentiment = positive - negative) %>%
  left_join(dooo_no_stop, by = 'title') %>%
  mutate(author_title = paste(author, ': ', title, sep = ''))

ggplot(article_sentiment, aes(author_title, sentiment)) +
  geom_bar(alpha = 0.8, stat = "identity", show.legend = FALSE) +
  xlab('author_title') +
  coord_flip()

# sentiment analysis by author

bing_words_per_author <- dooo_no_stop %>%
  inner_join(get_sentiments('bing')) %>%
  count(author)
colnames(bing_words_per_author) <- c('author', 'bing_words')

author_sentiment <- dooo_no_stop %>%
  filter(author != 'Mikhail Gershovich, Jim Groom, Mark Morvant, Jaimie Hoffman, David Morgen, Martha Burtis, Chris Mattia, Adam Croom, Tim Owens') %>%
  inner_join(get_sentiments("bing")) %>%
  count(author, sentiment) %>%
  spread(sentiment, n, fill = 0) %>%
  left_join(bing_words_per_author) %>%
  mutate(sentiment = (positive - negative) / bing_words,
         pos = sentiment >= 0)

ggplot(author_sentiment, aes(author, sentiment, fill = pos)) +
  geom_bar(alpha = 0.8, stat = "identity", show.legend = FALSE) +
  ylab('Sentiment: (positive words - negative words) / total sentiment-tagged words') +
  coord_flip()

# word cloud of most common positive/negative words

dooo_no_stop %>%
  inner_join(get_sentiments("bing")) %>%
  count(word, sentiment, sort = TRUE) %>%
  acast(word ~ sentiment, value.var = "n", fill = 0) %>%
  comparison.cloud(colors = c("#F8766D", "#00BFC4"),
                   max.words = 100)

# bigrams

dooo_bigrams <- as_tibble(dooo_texts) %>%
  transmute(author,
            title,
            url,
            date = as.Date(as.character(strptime(dooo_texts$date, '%m/%d/%Y'))),
            text = as.character(text)) %>%
  unnest_tokens(bigram, text, token = 'ngrams', n = 2) %>%
  separate(bigram, c("word1", "word2"), sep = " ") %>%
  filter(!word1 %in% c(stop_words$word, 'li', 'ul', 'http', 'htrf')) %>%
  filter(!word2 %in% c(stop_words$word, 'li', 'ul', 'http', 'htrf')) %>%
  unite(bigram, word1, word2, sep = ' ')

dooo_bigrams %>%
  count(bigram, sort = TRUE) %>%
  filter(n > 30) %>%
  mutate(bigram = reorder(bigram, n)) %>%
  ggplot(aes(bigram, n)) +
    geom_bar(alpha = 0.8, stat = "identity", show.legend = FALSE) +
    ylab('count') +
    coord_flip()

#umw authors only
dooo_bigrams %>%
  filter(author %in% umw_authors) %>%
  count(bigram, sort = TRUE) %>%
  filter(n > 25) %>%
  mutate(bigram = reorder(bigram, n)) %>%
  ggplot(aes(bigram, n)) +
  geom_bar(alpha = 0.8, stat = "identity", show.legend = FALSE) +
  ylab('count') +
  coord_flip()

#non-umw authors only
dooo_bigrams %>%
  filter(!author %in% umw_authors) %>%
  count(bigram, sort = TRUE) %>%
  filter(n > 9) %>%
  mutate(bigram = reorder(bigram, n)) %>%
  ggplot(aes(bigram, n)) +
  geom_bar(alpha = 0.8, stat = "identity", show.legend = FALSE) +
  ylab('count') +
  coord_flip()

dooo_bigrams %>%
  filter(author %in% c('Jim Groom', 'Tim Owens')) %>%
  count(bigram, sort = TRUE) %>%
  filter(n > 25) %>%
  mutate(bigram = reorder(bigram, n)) %>%
  ggplot(aes(bigram, n)) +
  geom_bar(alpha = 0.8, stat = "identity", show.legend = FALSE) +
  ylab('count') +
  coord_flip()

dooo_bigrams %>%
  filter(!author %in% c('Jim Groom', 'Tim Owens')) %>%
  count(bigram, sort = TRUE) %>%
  filter(n > 12) %>%
  mutate(bigram = reorder(bigram, n)) %>%
  ggplot(aes(bigram, n)) +
  geom_bar(alpha = 0.8, stat = "identity", show.legend = FALSE) +
  ylab('count') +
  coord_flip()

dooo_bigrams %>%
  filter(author %in% c('Jim Groom')) %>%
  count(bigram, sort = TRUE) %>%
  filter(n > 25) %>%
  mutate(bigram = reorder(bigram, n)) %>%
  ggplot(aes(bigram, n)) +
  geom_bar(alpha = 0.8, stat = "identity", show.legend = FALSE) +
  ylab('count') +
  coord_flip()

dooo_bigrams %>%
  filter(!author %in% c('Jim Groom')) %>%
  count(bigram, sort = TRUE) %>%
  filter(n > 13) %>%
  mutate(bigram = reorder(bigram, n)) %>%
  ggplot(aes(bigram, n)) +
  geom_bar(alpha = 0.8, stat = "identity", show.legend = FALSE) +
  ylab('count') +
  coord_flip()

# compare bigram frequency

umw_bigrams <- dooo_bigrams %>%
  filter(author %in% umw_authors)

no_umw_bigrams <- dooo_bigrams %>%
  filter(!author %in% umw_authors)

umw_bi_percent <- umw_bigrams %>%
  count(bigram) %>%
  transmute(bigram, umw_bi_freq = n / sum(n))

bi_frequency <- no_umw_bigrams %>%
  count(bigram) %>%
  mutate(other = n / sum(n)) %>%
  left_join(umw_bi_percent) %>%
  ungroup()

ggplot(bi_frequency, aes(x = other, y = umw_bi_freq, color = abs(umw_bi_freq - other))) +
  geom_abline(color = "gray40", lty = 2) +
  geom_jitter(alpha = 0.1, size = 2.5, width = 0.3, height = 0.3) +
  geom_text(aes(label = bigram), check_overlap = TRUE, vjust = 1.5) +
  scale_x_log10(labels = percent_format()) +
  scale_y_log10(labels = percent_format()) +
  scale_color_gradient(limits = c(0, 0.001), low = "darkslategray4", high = "gray75") +
  theme(legend.position="none") +
  labs(y = 'UMW authors', x = 'Everyone else')


# topic model

word_counts <- dooo_no_stop %>%
  anti_join(stop_words) %>%
  count(title, word, sort = TRUE) %>%
  ungroup()

dooo_dtm <- word_counts %>%
  cast_dtm(title, word, n)

dooo_lda <- LDA(dooo_dtm, k=16, control = list(seed=1234))

dooo_lda_td <- tidytext:::tidy.LDA(dooo_lda)

top_terms <- dooo_lda_td %>%
  group_by(topic) %>%
  top_n(10, beta) %>%
  ungroup() %>%
  arrange(topic, -beta)

top_terms %>%
  mutate(term = reorder(term, beta)) %>%
  ggplot(aes(term, beta, fill = factor(topic))) +
  geom_bar(alpha = 0.8, stat = "identity", show.legend = FALSE) +
  facet_wrap(~ topic, scales = "free") +
  coord_flip()

dooo_lda_gamma <- tidytext:::tidy.LDA(dooo_lda, matrix = "gamma")
colnames(dooo_lda_gamma) <- c('title', 'topic', 'gamma')
dooo_lda_gamma_meta <- dooo_lda_gamma %>%
  inner_join(unique(dooo_tidy %>% select(author, title, url, date) %>% group_by(title)))

dooo_classifications <- dooo_lda_gamma_meta %>%
  group_by(title) %>%
  top_n(1, gamma) %>%
  ungroup() %>%
  arrange(gamma)

dooo_classifications %>%
  ggplot(aes(topic)) +
  geom_bar()

dooo_classifications %>%
  filter(!author %in% c('Jim Groom', 'Mikhail Gershovich, Jim Groom, Mark Morvant, Jaimie Hoffman, David Morgen, Martha Burtis, Chris Mattia, Adam Croom, Tim Owens')) %>%
  count(author, topic, desc = TRUE) %>%
  ggplot(aes(author, n, fill = as.character(topic))) +
  geom_bar(stat = 'identity') +
  coord_flip() +
  guides(fill=guide_legend(title="Topic"))

author_class <- dooo_classifications %>%
  filter(!author %in% c('Jim Groom', 'Mikhail Gershovich, Jim Groom, Mark Morvant, Jaimie Hoffman, David Morgen, Martha Burtis, Chris Mattia, Adam Croom, Tim Owens')) %>%
  count(author, topic) %>%
  mutate(n = rescale(n)) 

dooo_classifications %>%
  filter(!author %in% c('Mikhail Gershovich, Jim Groom, Mark Morvant, Jaimie Hoffman, David Morgen, Martha Burtis, Chris Mattia, Adam Croom, Tim Owens')) %>%
  count(author, topic) %>%
  mutate(n = rescale(n)) %>%
  ggplot(aes(author, topic)) + 
    geom_tile(aes(fill = n),
              colour = "white") + 
    scale_fill_gradient(low = "white",
                      high = "steelblue") +
  scale_y_continuous(breaks=1:16) +
  coord_flip() +
  guides(fill=guide_legend(title="Proportion of\narticles in topic"))

# frequency change over time

words_by_time <- dooo_tidy %>%
  mutate(time_floor = floor_date(date, unit = "1 month")) %>%
  count(time_floor, word) %>%
  ungroup() %>%
  group_by(time_floor) %>%
  mutate(time_total = sum(n)) %>%
  group_by(word) %>%
  mutate(word_total = sum(n)) %>%
  ungroup() %>%
  rename(count = n) %>%
  filter(word_total > 30)

words_by_time_grouped <- dooo_tidy %>%
  mutate(time_floor = floor_date(date, unit = "1 month"),
         umw = (author %in% umw_authors)) %>%
  count(time_floor, umw, word) %>%
  ungroup() %>%
  group_by(umw, time_floor) %>%
  mutate(time_total = sum(n)) %>%
  group_by(word) %>%
  mutate(word_total = sum(n)) %>%
  ungroup() %>%
  rename(count = n) %>%
  filter(word_total > 30)

words_by_time %>%
  filter(word %in% c('reclaim', 'create')) %>%
  ggplot(aes(time_floor, count/time_total, color = word)) +
  geom_line(alpha = 0.8, size = 1.3) +
  labs(x = NULL, 
       y = 'Word frequency')

words_by_time %>%
  filter(word %in% c('umw', 'washington', 'ou', 'davidson', 'oklahoma', 'emory')) %>%
  ggplot(aes(time_floor, count/time_total, color = word)) +
  geom_line(alpha = 0.8, size = 1.3) +
  labs(x = NULL, 
       y = 'Word frequency')

words_by_time_grouped %>%
  filter(word %in% c('umw', 'washington', 'ou', 'davidson', 'oklahoma', 'emory'),
         umw == TRUE) %>%
  ggplot(aes(time_floor, count/time_total, color = word)) +
  geom_line(alpha = 0.8, size = 1.3) +
  labs(x = NULL, 
       y = 'Word frequency')

words_by_time_grouped %>%
  filter(word %in% c('umw', 'washington', 'ou', 'davidson', 'oklahoma', 'emory'),
         umw == FALSE) %>%
  ggplot(aes(time_floor, count/time_total, color = word)) +
  geom_line(alpha = 0.8, size = 1.3) +
  labs(x = NULL, 
       y = 'Word frequency')

dooo_tidy %>%
  mutate(umw = (author %in% umw_authors)) %>%
  group_by(umw) %>%
  count(date) %>%
  ggplot(aes(umw, date)) +
  geom_boxplot(alpha = 0.8) +
  xlab('UMW Author?') +
  ylab('Date') +
  coord_flip()
