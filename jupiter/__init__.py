#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Survaider
import hug

from huey import RedisHuey
from mongoengine import connect as mongo_connect

from jupiter._config import version, redis_params, mongo_params, mongo_dbi


huey = RedisHuey(**redis_params)

mongo_connect(mongo_dbi, **mongo_params)

# Register Huey tasks
import jupiter.tasks.periodic
import jupiter.tasks.utils

@hug.get('/', versions=1)
def index():
  return "Survaider"

# Register APIs
from jupiter.api import (
  hooks as api_hooks,
  tasks as api_tasks,
)

@hug.extend_api('/hooks')
def attach_hooks_api():
  return [api_hooks]

@hug.extend_api('/tasks')
def attach_tasks_api():
  return [api_tasks]

