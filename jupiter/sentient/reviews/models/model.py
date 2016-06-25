#!/usr/bin/env python
from mongoengine import *
# Connect to Database
#lazy connection
# connect("qwer")
class Reviews(DynamicDocument):
	"""docstring for Reviews"""
	
	provider=StringField()
	survey_id=StringField()
	rating=StringField()
	review=StringField()
	review_identifier=StringField()
	sentiment=StringField()
	date_added=StringField()
	datetime=DateTimeField()


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
class AspectQ(Document):
	base_url  = URLField(required=True)
	survey_id = StringField(required=True)
	unique_identifier=StringField(required=True,unique=True)
	parent= StringField() #Value , 'true'
	parent_id=StringField()
	status=StringField(default="false")
	last_update=DateTimeField()
	aspects=ListField(required=True)
	time_review= DateTimeField()
	meta = {'allow_inheritance': True}

	@property
	def repr(self):
		return {
			'id': str(self.pk),
			'access_url': self.base_url,
			'survey_id': self.survey_id,
			# 'children': self.children
		}

	def execute(self):
		# Get minute difference
		# fmt = '%Y-%m-%d %H:%M:%S'
		# now= datetime.now()
		# d1 = str(datetime.strptime(now, fmt))
		# d2 = str(datetime.strptime(self.last_update, fmt))

		# # convert to unix timestamp
		# d1_ts = time.mktime(d1.timetuple())
		# d2_ts = time.mktime(d2.timetuple())
		# minutes=int(d2_ts-d1_ts) / 60
		minutes=61
		# if self.status=="true" and minutes < MINUTES:
		if self.status=="true":
			print("Already Done",self.survey_id)
		else:
			if minutes>MINUTES:
				print ("Re-working")
			if self.parent=="true":
				survey_id=[self.survey_id]
				for obj in AspectQ.objects(parent_id=self.survey_id):
					survey_id.append(obj.survey_id)
			else:
				survey_id=self.survey_id
			try:
				print("provider",self.provider)
				Sentient(self.base_url,survey_id,self.provider).run()
				pass
			except Exception as e:
				print("EXECUTE Exception", e)
				raise e
			print("survey_id",survey_id)

class ZomatoQ(AspectQ):
	provider="zomato"
	def _scrape(self):
		pass

class TripAdvisorQ(AspectQ):
	provider="tripadvisor"
	def _scrape(self):
		pass

class HolidayIQQ(AspectQ):
	provider="holidayiq"
	def _scrape(self):
		pass

		