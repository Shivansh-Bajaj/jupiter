#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Survaider

"""Jupiter Task Runner - API endpoints.

This module provides interfaces to:
    - Add a task.
    - Get status.
    - Delete a task.
"""

from datetime import datetime
from bson import objectid

import hug
import falcon
from mongoengine import ValidationError, NotUniqueError
from pymongo import MongoClient

from jupiter._config import version, mongo_dbi, mongo_params, providers
from jupiter.api.directives import access_token
from jupiter.tasks.non_periodic import initial_data_download_and_ml_task

client = MongoClient(**mongo_params)
db = client[mongo_dbi]

# The data from a PUT or POST request in hug can be accessed by passing the
# name of the data element (for e.g., a key in case of json data) as an
# argument in the function decorated by a hug http router decorator.

def get_aspect_q_class(provider):
    return {
        'tripadvisor': 'AspectQ.TripAdvisorQ',
        'zomato': 'AspectQ.ZomatoQ',
        'HolidayIQ': 'AspectQ.HolidayIQQ',
        'booking': 'AspectQ.BookingQ'
    }.get(provider)

@hug.get('/{task_id}', versions=version)
def get_task(key: access_token, task_id: hug.types.text):
    pass

@hug.put('/', versions=version)
def put_task(key: access_token, obj_id: hug.types.text):
    # TODO: Check for validation errors (When the given parameters provided are
    # invalid).

    # Survaider saves the aspect_q objects.
    obj = db.aspect_q.find_one({'_id': objectid.ObjectId(obj_id)})
    initial_data_download_and_ml_task(obj)
    return {'success': 'Task successfully added'}

    # TODO: Return some identifier such as task id to the caller of api
    # so that it can later delete the task (if such a thing is allowed)
    # based on that identifier.
    # return {
	# 	'access_url': obj.base_url,
	# 	'survey_id': obj.survey_id,
    # }

"""Do NOT delete below commented put_task() function.
It is another version of the put_task() that may be used by third party users
of the jupiter api.
"""
# @hug.put('/', versions=version)
# def put_task(key: access_token,
#             provider: hug.types.one_of(providers),
#             access_url: hug.types.text,
#             survey_id: hug.types.text):
#     c = db.aspect_q.find({'unique_identifier': survey_id+provider}).count()
#     if c > 0:
#         raise falcon.HTTPBadRequest(title='Invalid survey_id',
#                                     description='The provided survey_id already exists')
#     # TODO: Check for validation errors (When the given parameters provided are
#     # invalid).
#     InsertOneResult_obj = db.aspect_q.insert_one({
#         '_cls': get_aspect_q_class(provider),
#         'survey_id': survey_id,
#         'base_url': access_url,
#         'unique_identifier': survey_id + provider,
#         'time_review': datetime(1980, 1, 1),
#         'last_update': datetime(1980, 1, 1),
#         'provider': provider
#     })
#     obj = db.aspect_q.find_one({'_id': InsertOneResult_obj.inserted_id})
#     initial_data_download_and_ml_task(obj)
#     # return {
# 	# 	'access_url': obj.base_url,
# 	# 	'survey_id': obj.survey_id,
#     # }
#     return {'success': 'Task successfully added'}
#     # TODO: Return some identifier such as task id to the caller of api
#     # so that it can later delete the task based on that identifier.

# providers = {'zomato': ZomatoQ, 'tripadvisor': TripAdvisorQ}
#
# @hug.put('/', versions=version)
# def put_task(key: access_token,
#             provider: hug.types.one_of(list(providers.keys())),
#             access_url: hug.types.text,
#             survey_id: hug.types.text,
#             children: hug.types.text,
#             time_review: hug.types.text):
#     provider_cls = providers[provider]
#     time_rev = datetime.striptime(time_review, "%Y-%m-%d")
#     # I can write the logic below? Right.--NO
#     aspects = aspects.split(",")
#
#     if provider == "zomato":
#         # Check if parent survey exists
#         parent = ZomatoQ.objects(unique_identifier = survey_id+provider).count()
#         try:
#             if parent != 1:
#                 obj = ZomatoQ()
#                 obj.base_url = access_url
#                 obj.survey_id = survey_id
#                 obj.parent = "true"
#                 obj.unique_identifier = survey_id + provider
#                 obj.time_review = time_rev
#                 obj.save()
#             obj2 = ZomatoQ()
#             obj2.base_url = access_url
#             obj2.survey_id = children
#             obj2.parent_id = survey_id
#             obj2.unique_identifier = children + provider
#             obj.time_review = time_rev
#             obj2.save()
#             return obj2.repr
#         except ValidationError:
#             raise falcon.HTTPBadRequest(title='ValidationError',
#                                         description='The parameters provided are invalid')
#         except NotUniqueError:
#             raise falcon.HTTPBadRequest(title='NotUniqueError',
#                                         description='The given survey_id exists')
#     elif provider == "tripadvisor":
#         parent = TripAdvisorQ.objects(unique_identifier=survey_id+provider).count()
#         try:
#             if parent != 1:
#                 obj = TripAdvisorQ()
#                 obj.base_url = access_url
#                 obj.survey_id = survey_id
#                 obj.parent = "true"
#                 obj.unique_identifier = survey_id + provider
#                 obj.time_review = time_rev
#                 obj.save()
#             obj2 = TripAdvisorQ()
#             obj2.base_url = access_url
#             obj2.survey_id = children
#             obj2.parent_id = survey_id
#             obj2.unique_identifier = children+provider
#             obj2.time_review = time_rev
#             obj2.save()
#             return obj2.repr
#         except ValidationError:
#             raise falcon.HTTPBadRequest(
#                 title='ValidationError',
#                 description='The parameters provided are invalid'
#             )
#         except NotUniqueError:
#             raise falcon.HTTPBadRequest(
#                 title='NotUniqueError',
#                 description='The given survey_id exists'
#             )

@hug.delete('/{task_id}', versions=version)
def delete_task(key: access_token, task_id: hug.types.text):
    pass
