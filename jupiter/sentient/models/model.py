from mongoengine import *
# Connect to Database
#lazy connection
connect("qwer")
class Status(Document):
	unique_identifier=StringField(unique=True)
	scraped_status=StringField()
	wc_status= StringField()
	reviewp_status= StringField()
	sentiment_status=StringField()
	aspectr_status= StringField()