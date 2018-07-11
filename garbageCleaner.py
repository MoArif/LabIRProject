#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  8 23:56:16 2018

@author: mofassir
"""
import re
from nltk.tokenize.moses import MosesDetokenizer

class garbageCleaner():
    emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

    regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs

    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
        ]

    detokenizer = None
    
    def __init__(self):
        print('Cleaner istance started')
        self.detokenizer = MosesDetokenizer()
        self.tokens_re = re.compile(r'('+'|'.join(self.regex_str)+')', re.VERBOSE | re.IGNORECASE)
        self.emoticon_re = re.compile(r'^'+self.emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

    def tokenize(self,s):
        s = re.sub(r'^https?:\/\/.*[\r\n]*', '', s, flags=re.MULTILINE)
        return self.tokens_re.findall(s)

    def remove_html(self,s):
        tokens = self.tokenize(s)
        for i in tokens:
            if i.find('http')  == 0 :
                tokens.remove(i)
        return tokens
    
    def remove_mentions(self,s):
        for i in s:
            if i.find('@') == 0 :
                s.remove(i)
        return s
      
    def preprocess(self,s, lowercase=False):
        tokens = self.tokenize(s)
        if lowercase:
            tokens = [token if self.emoticon_re.search(token) else token.lower() for token in tokens]
        return tokens
    
    def remove_emojis(self,s):
        s = re.sub(r'\W+', ' ', s)
        return s

    def detoken(self,token_input):
        return self.detokenizer.detokenize(token_input, return_str=True)
    
    def run_op(self,tweets_en):
        #tweets_en['text'][:] = [self.tokenize(s) for s in tweets_en['text']]
        tweets_en['text'][:] = [self.remove_html(s) for s in tweets_en['text']]
        tweets_en['text'][:] = [self.remove_mentions(s) for s in tweets_en['text']]
        tweets_en['text'][:] = [self.detoken(s) for s in tweets_en['text']]
        tweets_en['text'][:] = [self.remove_emojis(s) for s in tweets_en['text']]

        return tweets_en
        