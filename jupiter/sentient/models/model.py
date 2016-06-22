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