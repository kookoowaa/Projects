# Author.............: Park, Pablo Chanwoo
# File name..........: Twitter_crawler.py
# Written Date.......: 2018-12-20
# Program Description: Twitter crawler using API

# The crawler uses user-defined class "Easitter" made by Tomoya Fujita.
# Be sure to update Easitter.py with "your own credentials" before in use.
# Credentials may be put in command line using 'input()' command.

import Easitter
import pandas as pd
import re

# assign crawler instance
crawler = Easitter.Easitter()
# assign tag you wish to crawl
tag = input("tag for crawler: ")
# assign number of tweets you wish to crawl
n = int(input("number of tweets for crawling: "))

# run crawler
crawled = crawler.searchTweets(tag=tag, limit=n)

# Out of many information cralwed, retrieve the following data: 'date', 'tweet', 'language'.
date = [i['created_at'] for i in crawled]
text = [i['text'] for i in crawled]
lng = [i['lang'] for i in crawled]
# now rd is the DataFrame that contains useful data
rd = pd.DataFrame([date, text, lng]).T
rd.columns = ['date', 'text', 'lng']
rd.to_csv('tweets with tag-{}.csv'.format(tag))

# filter tweets with english only
eng_texts = rd[rd.lng=='en'].text.unique()
full_texts = []
for text in eng_texts:
    tmp = re.split('@[A-z0-9]*', text)[-1]
    tmp = re.sub(pattern = r'\n', string = tmp, repl =' ')
    tmp = re.sub(pattern = r'&amp;', string = tmp, repl ='&')
    tmp = re.split('[A-z]*…', tmp)[0]
    tmp = re.sub('http[A-z0-9:/.]*', string = tmp, repl='')
    tmp = re.sub('[!.\-,\'$()?:;"&/#+=]*', string = tmp, repl='')
    tmp = re.sub('^[ ]+', string = tmp, repl = '')
    tmp = re.sub('[ ]+$', string = tmp, repl = '')
    if len(tmp) >0:
        full_texts.append(tmp)
    
# write full_texts in txt file
temp_texts = [text + '\n' for text in full_texts]
fout = open('tweets with tag-{}.txt'.format(tag), 'w', encoding='utf-8')
fout.writelines(temp_texts)
fout.close()
print('==== Tweets clawed and saved at root directory ====\n')


# create wordcloud for visualization
import matplotlib.pyplot as plt
from wordcloud import WordCloud

## assign font and container attributes
font_path = 'c:\\windows\\fonts\\Roboto-Regular.ttf'
wordcloud = WordCloud(
    font_path = font_path,
   width = 800,
   height = 800
   )

## create wordcloud
long_text = ''
for text in full_texts:
    long_text = long_text + text
long_text = re.sub(tag, string = long_text.lower(), repl = '')

wordcloud = wordcloud.generate(long_text)
fig = plt.figure(figsize=(12,12))
plt.imshow(wordcloud)
plt.axis("off")

## save it on png
fig.savefig('wordcloud with tag-{}.png'.format(tag))
print('==== WordCloud from tweets generated and saved at root directory ====')