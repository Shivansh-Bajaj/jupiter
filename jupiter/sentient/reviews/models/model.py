#!/usr/bin/env python
from mongoengine import *
# Connect to Database
#lazy connection
# connect("qwer")
class Reviews(Document):
	"""docstring for Reviews"""
	
	provider=StringField()
	survey_id=StringField()
	rating=StringField()
	review=StringField()
	review_identifier=StringField()
	sentiment=StringField()
	date_added=StringField()
	datetime=DateTimeField()
	meta = {
		'indexes': [
			{'fields': ['-review_identifier'], 'unique': True,
			  'sparse': True, 'types': False },
		],
		'strict':False
	}


class Scraped(Document):
	provider=StringField()
	survey_id=StringField()
	status=StringField()
	# Maybe a time field?
class Record(Document):
	survey_id=StringField()
	rid=StringField()
	links=ListField()
	provider=StringField()
class WordCloudD(Document):
	"""docstring for WordCloud"""
	provider= StringField()
	survey_id=StringField()
	wc= DictField()
		