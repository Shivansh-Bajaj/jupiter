#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Survaider
"""Sentient Module
"""

from mongoengine import Document
from mongoengine.fields import URLField, DictField, BooleanField, StringField, ListField
from jupiter.sentient.models.model import Status
from jupiter.sentient.reviews.trippool import TripAdvisor
try:
  from jupiter.sentient.reviews.zomatopool import Zomato
except:
  from sentient.reviews.zomatopool import Zomato
from jupiter.sentient.reviews.nlp import WordCloud
from jupiter.sentient.aspect.reviewProcessing import ReviewP
from jupiter.sentient.aspect.sentimental import Sentiment
from jupiter.sentient.aspect.aspectratings import AspectR

class AspectQ(Document):
  base_url  = URLField(required=True)
  survey_id = StringField(required=True)
  unique_identifier=StringField(required=True,unique=True)
  parent= StringField() #Value , 'true'
  # unit_ids  =StringField()

  #Shouldn't there be a provider variable too?
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
    print (self.survey_id)
  def wordcloud(self):
    task= Status.objects(unique_identifier=self.survey_id+self.provider)
  def reviewp(self):
    task= Status.objects(unique_identifier=self.survey_id+self.provider)
    if task.scraped_status=="success" and task.reviewp_status!="success":
      ReviewP(self.survey_id,self.provider).run()
      task.update(reviewp_status="success")
    else:
      print ("ReviewP job ignored for ",self.survey_id,"provider",self.provider)
  def sentiment(self):
    task= Status.objects(unique_identifier=self.survey_id+self.provider)
    if task.scraped_status=="success" and task.reviewp_status=="success" and task.sentiment_status!="success":
      Sentiment(self.survey_id,self.provider).run()
      task.update(sentiment_status="success")
    else:
      print ("Sentiment job ignored for ",self.survey_id,"provider",self.provider)
  def aspectr(self):
    task= Status.objects(unique_identifier=self.survey_id+self.provider)
    if task.scraped_status=="success" and task.reviewp_status=="success" and task.sentiment_status=="success":
      AspectR(self.survey_id,self.provider)
      task.update(aspectr_status="success")
    else:
      print ("AspectR job ignored for ",self.survey_id,"provider",self.provider)


  def scrap(self):
    task= Status.objects(unique_identifier=self.survey_id+self.provider)
    if task.scraped_status=="success":
      print(self.survey_id,"ignored for provider",self.provider)
      pass
    else:
      if self.provider=="zomato":
        try:
          Zomato(self.base_url,self.survey_id,self.provider)
          Status(unique_identifier=self.survey_id+self.provider,scraped_status="success")
          
        except:
          print("Exception occured for ",self.survey_id,"provider",self.provider)
      elif self.provider=="tripadvisor":
        try:
          TripAdvisor(self.base_url,self.survey_id,self.provider)
          Status(unique_identifier=self.survey_id+self.provider,scraped_status="success")
        except:
          print("Exception occured for ",self.survey_id,"provider",self.provider)
      else:
        print("Bad Provider: ",self.provider)


    # self.provider would work.
   
    # HERE !!!!!!!
    # try:
    #   if self.survey_id=="lolo":
    #      return 1/0
    # except:
    #   print ("Exception handled for survey_id",self.survey_id)
    # if self.survey_id=="Queue Test":
    #   print("Queue")
    #   Sentient(self.base_url,self.survey_id,self.provider).run()
    # else:
    #   try:
    #     Sentient(self.base_url,self.survey_id,self.provider).run()
    #   except Exception as e:
    #     print ("Exception for survey_id",self.survey_id)

class Zomato(AspectQ):
  provider = 'zomato'
  def _scrape(self):
    # print("Zomato")
    pass
   # -> This is correct?: Sentient.run(self.base_url,self.survey_id,"zomato").run()
   #  print("Zomato")

class TripAdvisor(AspectQ):
  provider = 'tripadvisor'
  def _scrape(self):pass
    
    # print("TripAdvisor")
