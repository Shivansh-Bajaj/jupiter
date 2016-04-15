#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Survaider
"""Jupiter Task Runner API Base Interface

This module exists with following simple goals:
- Manage tasks with a set of credentials into the periodic task runners.
  - Credentials are the Zomato/Tripadvisor/etc. IDs and other informations
    that are sufficient to perform the aggregation tasks and any other stuff.
- Management provides the following interfaces via REST Endpoints:
  - Add a credential
  - Get the status
  - Revoke/Delete the task
- The API also provides an interface to subscribe to server webhooks which
  are sent to the requesting server when the tasks are completed.
  - Add a webhook subscription
  - Remove the subscription
"""
import hug
import falcon

from mongoengine import ValidationError, NotUniqueError

from jupiter._config import version
from jupiter.api.directives import access_token
from jupiter.sentient.model import Zomato, TripAdvisor

@hug.get('/{task_id}', versions=version)
def get_task(key: access_token, task_id: hug.types.text):
  pass

providers = {'zomato': Zomato, 'tripadvisor': TripAdvisor}

@hug.put('/', versions=version)
def put_task(key: access_token,
      provider: hug.types.one_of(list(providers.keys())),
      access_url: hug.types.text,
      survey_id: hug.types.text,
      children: hug.types.text):
  provider_cls = providers[provider]
  #I can write the logic below? Right.--NO
  if provider=="zomato":
      #Check if parent survey exists
      parent= Zomato.objects(unique_identifier= survey_id+provider).count()
      try:
          if parent!=1:
            obj=Zomato()
            obj.base_url = access_url
            obj.survey_id = survey_id
            obj.parent = "true"
            obj.unique_identifier=survey_id+provider
            obj.save()
            pass
          else:
            pass
          obj2= Zomato()
          obj2.base_url=access_url
          obj2.survey_id=children
          obj2.parent_id=survey_id
          obj2.unique_identifier=children+provider
          obj2.save()
          return obj2.repr
      except ValidationError:raise falcon.HTTPBadRequest(title='ValidationError',description='The parameters provided are invalid')
      except NotUniqueError:raise falcon.HTTPBadRequest(title='NotUniqueError',description='The given survey_id exists')
  elif provider=="tripadvisor":
    parent= TripAdvisor.objects(unique_identifier=survey_id+provider).count()
  try:
    if parent!=1:
      obj = TripAdvisor()
      obj.base_url = access_url
      obj.survey_id = survey_id
      obj.parent ="true"
      obj.unique_identifier=survey_id+provider
      obj.save()
    else:pass
    obj2=TripAdvisor()
    obj2.base_url=access_url
    obj2.survey_id=children
    obj2.parent_id=survey_id
    obj2.unique_identifier=children+provider
    obj2.save()
    return obj2.repr
  except ValidationError:
    raise falcon.HTTPBadRequest(
        title='ValidationError',
        description='The parameters provided are invalid')

  except NotUniqueError:
    raise falcon.HTTPBadRequest(
        title='NotUniqueError',
        description='The given survey_id exists')


@hug.delete('/{task_id}', versions=version)
def delete_task(key: access_token, task_id: hug.types.text):
  pass
