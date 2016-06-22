#!/usr/bin/env python
from mongoengine import *
# Connect to Database
#lazy connection
# connect("qwer")
class Aspect(Document):
	"""docstring for Aspect"""
	sector=StringField()
	# food=StringField()
	# service=StringField()
	# price=StringField()
	ambience=StringField()
	value_for_money=StringField()
	room_service=StringField()
	cleanliness=StringField()
	amenities=StringField()
	
	overall=StringField()
	survey_id=StringField()
	provider=StringField()
class Reviews(Document):
	"""docstring for Reviews"""
	provider=StringField()
	survey_id=StringField()
	rating=StringField()
	review=StringField()
	review_identifier=StringField()
	sentiment= StringField()
	meta = {
		'indexes': [
			{'fields': ['-review_identifier'], 'unique': True,
			  'sparse': True, 'types': False },
		],
	}
class ChiFinal(Document):
	data=ListField(unique=True)
	survey_id=StringField()
	provider=StringField()
class ExpKeywords(Document):
	"""ExpendedAspectKeywords"""
	pass
class SentR(Document):
	"""docstring for Sentimental Reviews"""
	# sentence=StringField()
	# sentiment=StringField()
	line=ListField()
	survey_id=StringField()
	provider=StringField()
class WordCloud(Document):
	provider=StringField()
	survey_id=StringField()
	wordcloud=DictField()

class Sentiments(Document):
	survey_id=StringField()
	provider=StringField()
	review=StringField()
	sentiment=StringField()