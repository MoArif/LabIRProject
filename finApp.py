#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 19:56:39 2018

@author: mofassir
"""
from gensim import utils
from gensim.models.doc2vec import LabeledSentence
from gensim.models import Doc2Vec

# numpy
import numpy

# classifier
from sklearn.linear_model import LogisticRegression

# random
import random


class LabeledLineSentence():
    def __init__(self, sources):
        self.sources = sources
        
        flipped = {}
        
        # make sure that keys are unique
        for key, value in sources.items():
            if value not in flipped:
                flipped[value] = [key]
            else:
                raise Exception('Non-unique prefix encountered')
    
    def __iter__(self):
        for source, prefix in self.sources.items():
            with utils.smart_open(source) as fin:
                for item_no, line in enumerate(fin):
                    yield LabeledSentence(utils.to_unicode(line).split(), [prefix + '_%s' % item_no])
    
    def to_array(self):
        self.sentences = []
        for source, prefix in self.sources.items():
            with utils.smart_open(source) as fin:
                for item_no, line in enumerate(fin):
                    self.sentences.append(LabeledSentence(utils.to_unicode(line).split(), [prefix + '_%s' % item_no]))
        return self.sentences
    
    def sentences_perm(self):
        shuffled = list(self.sentences)
        random.shuffle(shuffled)
        return shuffled




sources = {'sad_tweets_test.txt':'TEST_NEG', 'happy_tweets_test.txt':'TEST_POS', \
           'sad_tweets.txt':'TRAIN_NEG', 'happy_tweets.txt':'TRAIN_POS'}

sentences = LabeledLineSentence(sources)
#model = Doc2Vec(min_count=1, window=10, size=150, sample=1e-4, negative=5, workers=7)
#
#model.build_vocab(sentences.to_array())
#
#
#model.train(sentences.sentences_perm(),total_examples=25000,epochs=50)

model = Doc2Vec.load('../Finmodel.d2v')
train_arrays = numpy.zeros((25000, 150))
train_labels = numpy.zeros(25000)

for i in range(12500):
    prefix_train_pos = 'TRAIN_POS_' + str(i)
    prefix_train_neg = 'TRAIN_NEG_' + str(i)
    train_arrays[i] = model[prefix_train_pos]
    train_arrays[12500 + i] = model[prefix_train_neg]
    train_labels[i] = 1
    train_labels[12500 + i] = 0

test_arrays = numpy.zeros((20, 150))
test_labels = numpy.zeros(20)

for i in range(10):
    prefix_test_pos = 'TEST_POS_' + str(i)
    prefix_test_neg = 'TEST_NEG_' + str(i)
    test_arrays[i] = model[prefix_test_pos]
    test_arrays[10 + i] = model[prefix_test_neg]
    test_labels[i] = 1
    test_labels[10 + i] = 0

classifier = LogisticRegression(solver='lbfgs')
classifier.fit(train_arrays, train_labels)