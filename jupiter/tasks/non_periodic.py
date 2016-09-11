#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Survaider

"""
This module defines huey tasks that are run once with optional retries and delays.
"""

import datetime

from huey import crontab
from pymongo import MongoClient

from jupiter import huey
from jupiter._config import mongo_params, mongo_dbi
from jupiter.tasks.jobs import download_data_and_run_ml

# Connect to database
client = MongoClient(mongo_params['host'], mongo_params['port'])
db = client[mongo_dbi]

@huey.task()
def initial_data_download_and_ml_task(obj):
	download_data_and_run_ml(obj)
	db.aspect_q.update_one({
			'_id': obj['_id']
		}, {
			'$set': {
				'last_update': datetime.datetime.now()
			}
		}, upsert=False)
