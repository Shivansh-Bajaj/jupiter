from mongoengine import *
# Connect to Database
#lazy connection
# connect("qwer")
class Status(Document):
	unique_identifier=StringField(unique=True)
	scraped_status=StringField(default="false")
	wc_status= StringField(default="false")
	reviewp_status= StringField(default="false")
	sentiment_status=StringField(default="false")
	aspectr_status= StringField(default="false")
class WStatus(Document):
	unique_identifier=StringField(unique=True)
	status= StringField(default="false")
class Bootstrap(Document):
	aspects=DictField(required=True)
	inuse=StringField()
# class AspectQ(Document):
# 	base_url  = URLField(required=True)
# 	survey_id = StringField(required=True)
# 	unique_identifier=StringField(required=True,unique=True)
# 	parent= StringField() #Value , 'true'
# 	parent_id=StringField()
# 	status=StringField(default="false")
# 	aspects= ListField()
# 	last_update=DateTimeField()
# 	meta = {'allow_inheritance': True}

class SurveyAspects(Document):
	survey_id=StringField(required=True)
	aspects=ListField(required=True)