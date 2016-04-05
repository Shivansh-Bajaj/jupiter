#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Survaider
import hug

from huey import RedisHuey

from jupiter._config import version, redis_params


huey = RedisHuey(**redis_params)


@hug.get('/', versions=1)
def index():
  return "Survaider"

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

