#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 17:25:29 2018

@author: mofassir
"""
import numpy as np
import json
import pandas as pd
import re
import matplotlib.pyplot as plt
from nltk.tokenize.moses import MosesDetokenizer
from garbageCleaner import garbageCleaner
from Hashtag_gen import Hashtags
from countryList import Country_gen
import re


def file_read(filepath):
    tweets_data = []
    tweets_file = open(filepath, "r")
    hit_count = 0
    miss_count = 0
    len_count = 0

    for line in tweets_file:
        len_count+=1
        if len_count ==100000000:
            break
        try:
            tweet = json.loads(line)
            tweets_data.append(tweet)
            hit_count+=1
        except:
            miss_count+=1
            continue
    return tweets_data,(len_count,hit_count,miss_count)

def decoding_file(tweets_data):
    """
    This functions takes in a file and decodes a dataframe with the tweet text,
    language and country
    args:
        tweet_data =  tweet Json file
    returns:
        data_df = pandas data frame with tweet, lang and country
    """
    ht_gen = Hashtags()
    country_gen = Country_gen()
    text = [x['text'] for x in tweets_data]
    lang = [x['lang'] for x in tweets_data]
    country = [ x['place']['country'] if x['place'] != None else              \
                                 country_gen.getCountry() for x in tweets_data]
    follower_count = [x['user']['followers_count'] for x in tweets_data]
    timeMs = [x['timestamp_ms'] for x in tweets_data]
    hashTags = [ x['entities']['hashtags'][0]['text'] if                      \
                len(x['entities']['hashtags']) != 0 else ht_gen.getHashtag()  \
                                                          for x in tweets_data]
    tweets = pd.DataFrame([text,lang,country,follower_count,timeMs,hashTags], \
                              index=['text','lang','country','follower_count',\
                                                        'timeMs','hashtags']).T

    return tweets

 
def main():
    #fp = 'tweet_data.txt'
    #fp = 'tweet_happy.txt'
    fp = 'tweet_sad.txt'
    Tweet_data_Test,counts = file_read(fp)
    tweets = decoding_file(Tweet_data_Test)
    print('happy Tweet: ', len(tweets))
    print('removing non english: ')
    tweets_en = tweets[tweets['lang'][:] =='en'] 
    print('English Tweets: ',len(tweets_en))
    print('Making Grabage Cleaner for data cleaning: ')
    cleaner = garbageCleaner()
    fin  = cleaner.run_op(tweets_en.iloc[:][0:25000]) 
    np.savetxt('sad_tweets.txt',fin,fmt='%s',delimiter=',')

if __name__ == "__main__":
    main()