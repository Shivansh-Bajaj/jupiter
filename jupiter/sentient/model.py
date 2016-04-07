#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Survaider
"""Sentient Module
"""

from mongoengine import Document
from mongoengine.fields import URLField, DictField, BooleanField, StringField, ListField


class Aspect(Document):
  base_url  = URLField(required=True)
  survey_id = StringField(required=True, unique=True)
  unit_ids  = ListField(StringField())

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
    print(self.survey_id)

class Zomato(Aspect):
  def _scrape(self):
    pass

class TripAdvisor(Aspect):
  def _scrape(self):
    pass

