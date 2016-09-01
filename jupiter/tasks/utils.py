#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Survaider

import requests

from jupiter import huey


@huey.task(retries=3, retry_delay=10)
def async_get(*pa, **kwa):
  requests.get(*pa, **kwa)

@huey.task(retries=3, retry_delay=10)
def async_post(*pa, **kwa):
  requests.post(*pa, **kwa)
