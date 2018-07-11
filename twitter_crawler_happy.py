#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 17:09:46 2018

@author: mofassir
"""

import numpy as np
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API 
access_token = "234320725-g93nFxNG0uhqK6hdTzjIaWUY4e3H1wZRr9o5Hj8P"
access_token_secret = "5nbWodpazCfMZue9lZImgkelZOx06vSv5jfqYWSdAhYFb"
consumer_key = "TbU74PUrtQnIx1MsoC3Z4AW3V"
consumer_secret = "lSzIIsMq9pFkXZWm15txErIIibMwIwRb8mqL8vF5dDSIQrjtph"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=[':(', ':-(', ':(',':\'('])