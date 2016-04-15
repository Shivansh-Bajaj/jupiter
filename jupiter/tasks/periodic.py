#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Survaider
from huey import crontab

from jupiter import huey
from jupiter.sentient.model import AspectQ

@huey.periodic_task(crontab(minute='*/2'))
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
  print ("Process Running-- delay : 2min")
  for obj in AspectQ.objects:
    obj.reviewp()
  pass

@huey.periodic_task(crontab(minute='*/1'))
def spawn_processor_m_15():
  """These processors are run every 15 minutes

  Processors Index
  ----------------
  These processors are explicitly run:
  - (Extend this list as needed)
  """
  for obj in AspectQ.objects:
    obj.scrap()
  pass

@huey.periodic_task(crontab(minute='*/1'))
def spawn_processor_m_45():
  """
  These processors are run every 45 minutes.
  This is the next step after aspectr.

  """
  for obj in AspectQ.objects:
    obj.sentiment
  pass

@huey.periodic_task(crontab(minute='*/60'))
def spawn_processor_m_60():
  """
  These processors are run every 60 minutes.
  This is the next step after sentiment.
  Takes a long time.

  """
  for obj in AspectQ.objects:
    obj.aspectr
  pass

