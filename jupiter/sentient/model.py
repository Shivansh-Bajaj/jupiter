#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Survaider
"""Sentient Module
"""

from mongoengine import Document
from mongoengine.fields import (URLField, DictField, BooleanField, StringField,
    ListField, DateTimeField)
from datetime import datetime
import time
# from jupiter.sentient.models.model import WStatus


class AspectQ(Document):
	base_url = URLField(required=True)
	survey_id = StringField(required=True)
	unique_identifier = StringField(required=True, unique=True)
	parent = StringField() # Value,'true'
	parent_id = StringField()
	status = StringField(default="false")
	last_update = DateTimeField(default='1980-01-01')
	aspects = ListField(required=False)
	time_review = DateTimeField()
	aspect_notation = ListField()

	meta = {'allow_inheritance': True}
