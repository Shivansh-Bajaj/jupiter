#!/usr/bin/env python
from mongoengine import *

# Connect to Database
# lazy connection
# connect("qwer")

class Reviews(DynamicDocument):
	"""docstring for Reviews"""
	provider = StringField()
	survey_id = StringField()
	rating = StringField()
	review = StringField()
	review_identifier = StringField()
	sentiment = StringField()
	date_added = DateTimeField()
	review_link = StringField()
	datetime = DateTimeField()

class Scraped(Document):
	provider = StringField()
	survey_id = StringField()
	status = StringField()
	# Maybe a time field?

class Record(Document):
	survey_id = StringField()
	rid = StringField()
	links = ListField()
	provider = StringField()

class WordCloudD(Document):
	"""docstring for WordCloud"""
	provider = StringField()
	survey_id = StringField()
	wc = DictField()

class AspectsPolarityCount(Document):
	review_obj_id = StringField(unique=True)
	hashtable = DictField()
	# Structure of `hashtable` field:
	# {
	# 	'aspect_name_1': [positives_count, negatives_count, neutral_count],
	# 	...
	#	...
	# 	'aspect_name_n': [positives_count, negatives_count, neutral_count]
	# }
