#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Survaider
"""Webhook Register

This module is used to register the webhooks.

"""
from mongoengine import Document, StringField, ListField, DictField

from jupiter.tasks.utils import async_post

scope_values = []


class Hook(Document):
  callback = StringField(required=True)
  payload = DictField()
  # signal = ListField()

  meta = {'allow_inheritance': True}

  @property
  def repr(self):
    return {
      'id': str(self),
      'target': self.callback,
    }

  def execute(self):
    # Ping the server
    # async_post()
    pass
