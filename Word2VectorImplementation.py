#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 17:25:52 2018

@author: mofassir
"""

from sklearn.feature_extraction.text import CountVectorizer
from gensim.models import Word2Vec
import pandas as pd
import numpy as np
from gensim.models import word2vec
import nltk
from sklearn.decomposition import PCA
from matplotlib import pyplot
def readfile(fp):
    df = pd.read_csv(fp[0],delimiter=',',header=None).fillna('This is a tweet')
    df2 = pd.read_csv(fp[1],delimiter=',',header=None).fillna('This is a tweet')
    return pd.concat([df,df2])

corpus = [
          'Text of the first document.',
          'Text of the second document made longer.',
          'Number three.',
          'This is number four.',
]
# we need to pass splitted sentences to the model

def vectorizer(corpus):
    tokenized_sentences = [str(sentence).split() for sentence in corpus]
    model = word2vec.Word2Vec(tokenized_sentences,size=150,min_count=1,sg=1,window=10)
    return model

def old():
    tokenized_sentences = [str(sentence).split() for sentence in corpus]
    model = word2vec.Word2Vec(tokenized_sentences,size=6,min_count=1,sg=1)
    
    print('model: \n',model)
    # summarize vocabulary
    words = list(model.wv.vocab)
    print('words: \n ',words)
    # access vector for one word
    print(model['Text'])
    # save model
    model.save('tempmodel.bin')
    model.wv.save_word2vec_format('tempmodel.txt', binary=False)
    # load model
    new_model = Word2Vec.load('tempmodel.bin')
    #print(new_model)
    return

def main():
    fp = ['sad_tweets.txt','happy_tweets.txt']
    df = readfile(fp)
    model = vectorizer(df[0][:])
    model.train(df[0][:],total_examples=18000,epochs=10)
    
    X = model[model.wv.vocab]
    pca = PCA(n_components=2)
    result = pca.fit_transform(X)
    # create a scatter plot of the projection
    pyplot.scatter(result[:, 0], result[:, 1])
    words = list(model.wv.vocab)
    for i, word in enumerate(words):
        pyplot.annotate(word, xy=(result[i, 0], result[i, 1]))
    pyplot.show()
if __name__ == "__main__":
    main()