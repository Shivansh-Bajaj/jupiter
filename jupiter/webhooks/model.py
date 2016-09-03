#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Survaider

"""Webhook Register

This module is used to register the webhooks.
"""

from mongoengine import Document
from mongoengine.fields import URLField, DictField, BooleanField, StringField

from jupiter.tasks.utils import async_post


# Define all the events that may be subscribed to
scope_values = [
    'scraped', # Emit this when a scraping task is finished.
]

def emit(scope, callback, **kwa):
    """Helper method to emit the events"""
    hook = Hook.objects(scope=scope, callback=callback)
    try:
        hook = hook[0]
        if not hook.active:
            raise RuntimeError
        hook.payload.update(kwa)
        hook.save()
        hook.execute()
    except (KeyError, RuntimeError):
        raise ValueError('No such scope-callback combination exist')

class Hook(Document):
    callback = URLField(required=True, unique_with='scope')
    scope = StringField(required=True, choices=scope_values)
    payload = DictField()
    active = BooleanField(default=True)

    meta = {'allow_inheritance': True}

    @property
    def repr(self):
        return {
            'id': str(self.id),
            'callback': self.callback,
        }

    def execute(self):
    # Send the webhook request
        async_post(self.callback, data=self.payload)
