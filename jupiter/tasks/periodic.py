#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Survaider

import datetime

from huey import crontab
from pymongo import MongoClient

from jupiter import huey
from jupiter.sentient.main import Sentient
from jupiter._config import mongo_params, mongo_dbi

# Get database
client = MongoClient(mongo_params['host'], mongo_params['port'])
db = client[mongo_dbi]


# This is the renamed `execute()` method of `AspectQ` objects.
def download_data_and_run_ml(obj):
    # Get minute difference
    # fmt = '%Y-%m-%d %H:%M:%S'
    # now = datetime.now()
    # d1 = str(datetime.strptime(now, fmt))
    # d2 = str(datetime.strptime(self.last_update, fmt))

    # # Convert to unix timestamp
    # d1_ts = time.mktime(d1.timetuple())
    # d2_ts = time.mktime(d2.timetuple())
    # minutes = int(d2_ts-d1_ts) / 60
    try:
        parent_id = db.relation.find_one({'survey_id': obj['survey_id']})['parent_id']
        aspects = db.client_aspects.find_one({'parent_id': parent_id})['aspects']
    except Exception as e:
        print('\n\n --- EXCEPTION --- \n', e, '\n\n')
        raise e
    try:
        print("provider", obj['provider'])
        Sentient(obj['base_url'], obj['survey_id'], obj['provider'], aspects).run()
    except Exception as e:
        print('\n\n --- EXCEPTION --- \n', e, '\n\n')
        raise e
    print("survey_id", obj['survey_id'])


@huey.periodic_task(crontab(minute='*/1'))
def spawn_processor_m_30():
    """These processors are run every 30 minutes

    Processors Index
    ----------------
    These processors are explicitly run:
    - External API Calls
    - (Extend this list as needed)

    Developer Notes
    ---------------
    All the tasks (such as scraping, or, machine learning etc.) must be *spawned*
    from here. It is important to note that these tasks are **required** to be
    non-blocking and must be huey tasks.

    To prevent any magic to happen, do **not** spawn any periodic tasks inside.
    """
    print("Process Running -- delay : 2min")
    for obj in db.aspect_q.find():
        try:
            download_data_and_run_ml(obj)
            obj['last_update'] = datetime.datetime.now()
            obj.save()
            print("success", obj['survey_id'])
        except Exception as e:
            print ("An exeption occured while executing survey_id", obj['survey_id'])


# @huey.periodic_task(crontab(minute='*/1'))
# def spawn_processor_m_15():
#     """These processors are run every 15 minutes
#
#     Processors Index
#     ----------------
#     These processors are explicitly run:
#     - (Extend this list as needed)
#     """
#     for obj in AspectQ.objects:
#     obj.scrap()
#     pass
#
# @huey.periodic_task(crontab(minute='*/45'))
# def spawn_processor_m_45():
#     """
#     These processors are run every 45 minutes.
#     This is the next step after aspectr.
#
#     """
#     # for obj in AspectQ.objects:
#     #   obj.sentiment
#     pass


@huey.periodic_task(crontab(minute='*/60'))
def spawn_processor_m_60():
    """
    Task to check for new reviews on TA
    """
    # for obj in AspectQ.objects:
    #   obj.aspectr
    pass
