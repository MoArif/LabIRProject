#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 15:01:00 2018

@author: mofassir
"""
import random
class Country_gen():
    country_list = ['South Africa',
 'United States',
 '',
 'Canada',
 'Brasil',
 'India',
 'Danmark',
 'The Netherlands',
 'Malaysia',
 'United Kingdom',
 '대한민국',
 'Germany',
 'Republic of the Philippines',
 'Russia',
 'Deutschland',
 'Poland',
 'Россия',
 'Italia',
 "Democratic People's Republic of Korea (North Korea)",
 'Austria',
 'France',
 'Indonesia',
 'Bosnia and Herzegovina',
 'Singapore',
 'Republic of Serbia',
 'Mexico',
 'Pakistan',
 'México',
 "People's Republic of China",
 'Spain',
 'Vereinigte Staaten',
 'Hungary',
 'Nepal']
    def __init__(self):
        print('Hashtag Corpus initialized')
    def getCountry(self):
        return self.country_list[random.randint(0,len(self.country_list)-1)]