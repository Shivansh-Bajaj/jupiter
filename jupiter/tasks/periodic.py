#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Survaider

"""
This module defines periodic huey tasks.
"""

import datetime

from huey import crontab
from pymongo import MongoClient

from jupiter import huey
from jupiter.sentient.main import Sentient
from jupiter._config import mongo_params, mongo_dbi

from jupiter.tasks.jobs import download_data_and_run_ml


# Connect to database
client = MongoClient(mongo_params['host'], mongo_params['port'])
db = client[mongo_dbi]

@huey.periodic_task(crontab(minute='*/30'))
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
    from within here. It is important to note that these tasks are **required**
    to be non-blocking and must be huey tasks.

    To prevent any magic to happen, do **not** spawn any periodic tasks inside here.
    """
    print('Process Running -- delay : 1min')    # From arg to crontab.
    for obj in db.aspect_q.find():
        download_data_and_run_ml(obj)
        db.aspect_q.update_one({
                '_id': obj['_id']
            }, {
                '$set': {
                    'last_update': datetime.datetime.now()
                }
            }, upsert=False)

# @huey.periodic_task(crontab(minute='*/15'))
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
#
# @huey.periodic_task(crontab(minute='*/60'))
# def spawn_processor_m_60():
#     """
#     Task to check for new reviews on TA
#     """
#     # for obj in AspectQ.objects:
#     #   obj.aspectr
#     pass
