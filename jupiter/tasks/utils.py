#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Survaider

import requests

from jupiter import huey

@huey.task(retries=3, retry_delay=10)
def async_get(*args, **kwargs):
    requests.get(*args, **kwargs)

@huey.task(retries=3, retry_delay=10)
def async_post(*args, **kwargs):
    requests.post(*args, **kwargs)
