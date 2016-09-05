#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Survaider

"""
This module defines the functions and classes that are run by huey tasks.
"""

from pymongo import MongoClient

from jupiter.sentient.main import Sentient
from jupiter._config import mongo_params, mongo_dbi


# Connect to database
client = MongoClient(mongo_params['host'], mongo_params['port'])
db = client[mongo_dbi]


def download_data_and_run_ml(obj):
    parent_id = db.relation.find_one({'survey_id': obj['survey_id']})['parent_id']
    aspects = db.client_aspects.find_one({'parent_id': parent_id})['aspects']
    Sentient(obj['base_url'], obj['survey_id'], obj['provider'], aspects).run()


if __name__ == '__main__':
	print('This module is not intended to be run explicitly. '
			'Import the functions and classes instead.')
