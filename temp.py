"""
File for temporary manual testing.
"""

from datetime import datetime

import hug
import falcon
from pymongo import MongoClient

from jupiter.api.directives import access_token
from jupiter._config import version, mongo_dbi, mongo_params, providers


client = MongoClient(**mongo_params)
db = client[mongo_dbi]


def get_aspect_q_class(provider):
    return {
        'tripadvisor': 'AspectQ.TripAdvisorQ',
        'zomato': 'AspectQ.ZomatoQ',
        'HolidayIQ': 'AspectQ.HolidayIQQ',
        'booking': 'AspectQ.BookingQ'
    }.get(provider)


@hug.put('/')
def put_task(key: access_token,
            provider: hug.types.one_of(providers),
            access_url: hug.types.text,
            survey_id: hug.types.text):
    c = db.aspect_q.find({'unique_identifier': survey_id+provider}).count()
    if c > 0:
        raise falcon.HTTPBadRequest(title='Invalid survey_id',
                                    description='The provided survey_id already exists')
    obj = db.aspect_q.insert_one({
        '_cls': get_aspect_q_class(provider),
        'survey_id': survey_id,
        'base_url': access_url,
        'unique_identifier': survey_id + provider,
        'time_review': datetime(1980, 1, 1),
        'last_update': datetime(1980, 1, 1),
        'provider': provider
    })
    # return {
	# 	'access_url': obj.base_url,
	# 	'survey_id': obj.survey_id,
    # }
    return {'success': 'Task successfully added'}
