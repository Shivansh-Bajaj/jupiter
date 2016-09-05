#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Survaider

version = 1

access_tokens = {
    'c6b6ab1e-cab4-43e4-9a33-52df602340cc': {
        'user': 'debugger',
        'generated': '20160405',
        'access': 777,
        'active': True
    }
}

redis_params = {
    'host': 'localhost',
    'port': '6379'
}

mongo_params = {
    'host': 'localhost',
    'port': 27017
}

mongo_dbi = 'qwer'  # Should be same as the survaider-app

providers = ['zomato', 'tripadvisor']
