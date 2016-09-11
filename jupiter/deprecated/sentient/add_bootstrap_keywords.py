#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Survaider

import re

from mongoengine import connect

# from _config import mongo_params,mongo_dbi
from jupiter.sentient.models.model import Bootstrap

filename="aspect/Data/restaurant_bootstrapping.dat"
connect('lolwa')
f = open(filename, 'r')
aspects={}
for line in f.readlines():
    container = line.split(" ")
    keywords = []
    for i in range(1,len(container)):
    	word=container[i].strip()
    	if len(word)!=0:
        	keywords.append(word)
    asp_name = re.sub("[:]", "" , container[0])
    aspects[asp_name]=keywords
Bootstrap(aspects=aspects,inuse="true").save()
print("Done")
