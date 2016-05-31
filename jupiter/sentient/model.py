
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Survaider
"""Sentient Module
"""

from mongoengine import Document
from mongoengine.fields import URLField, DictField, BooleanField, StringField, ListField,DateTimeField
from datetime import datetime
import time
try:
	from jupiter.sentient.main import Sentient
	from jupiter.sentient.models.model import WStatus
except:
	from main import Sentient
	from models.model import WStatus

"""
HARD VARIABLES
"""
MINUTES=60
class AspectQ(Document):
	base_url  = URLField(required=True)
	survey_id = StringField(required=True)
	unique_identifier=StringField(required=True,unique=True)
	parent= StringField() #Value , 'true'
	parent_id=StringField()
	status=StringField(default="false")
	last_update=DateTimeField()
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
		fmt = '%Y-%m-%d %H:%M:%S'
		now= datetime.datetime.now()
		d1 = datetime.strptime(now, fmt)
		d2 = datetime.strptime(self.last_update, fmt)

		# convert to unix timestamp
		d1_ts = time.mktime(d1.timetuple())
		d2_ts = time.mktime(d2.timetuple())
		minutes=int(d2_ts-d1_ts) / 60
		if self.status=="true" and minutes < MINUTES:
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
