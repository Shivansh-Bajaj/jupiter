
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Survaider
"""Sentient Module
"""

from mongoengine import Document
from mongoengine.fields import URLField, DictField, BooleanField, StringField, ListField
from jupiter.sentient.main import Sentient
from jupiter.sentient.models.model import WStatus
class AspectQ(Document):
  base_url  = URLField(required=True)
  survey_id = StringField(required=True)
  unique_identifier=StringField(required=True,unique=True)
  parent= StringField() #Value , 'true'
  parent_id=StringField()
  status=StringField(default="false")
  meta = {'allow_inheritance': True}

  @property
  def repr(self):
    return {
      'id': str(self.pk),
      'access_url': self.base_url,
      'survey_id': self.survey_id,
      'children': self.unit_ids
    }

  def execute(self):
    if self.status==True:
      print("Already Done",self.survey_id)
    else:
      if self.parent=="true":
        survey_id=[self.survey_id]
        for obj in AspectQ.objects(parent=self.survey_id):
          survey_id.append(obj.survey_id)

      try:
        Sentient(self.base_url,self.survey_id,self.provider).run()


        pass
      except Exception as e:
        raise e

      print(self.survey_id)

class ZomatoQ(AspectQ):
  provider="zomato"
  def _scrape(self):
    pass

class TripAdvisorQ(AspectQ):
  provider="tripadvisor"
  def _scrape(self):
    pass
