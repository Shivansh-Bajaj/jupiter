#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Survaider
from huey import crontab

from jupiter import huey
from jupiter.sentient.model import AspectQ
import datetime
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
  print ("Process Running-- delay : 2min")
  # print(len(AspectQ.objects))

  for obj in AspectQ.objects:
    try:
      obj.execute()
      # obj.status="true"
      obj.last_update=datetime.datetime.now()
      obj.save()
      # obj(status="true").save()
      print("success",obj.survey_id)
    except Exception as e:
      # print ("Exception",e,obj.survey_id)
      print ("An exeption occured while executation for survey_id",obj.survey_id)
      
  pass

# @huey.periodic_task(crontab(minute='*/1'))
# def spawn_processor_m_15():
#   """These processors are run every 15 minutes

#   Processors Index
#   ----------------
#   These processors are explicitly run:
#   - (Extend this list as needed)
#   """
#   for obj in AspectQ.objects:
#     obj.scrap()
#   pass

# @huey.periodic_task(crontab(minute='*/45'))
# def spawn_processor_m_45():
#   """
#   These processors are run every 45 minutes.
#   This is the next step after aspectr.

#   """
#   # for obj in AspectQ.objects:
#   #   obj.sentiment
#   pass

@huey.periodic_task(crontab(minute='*/60'))
def spawn_processor_m_60():
  """
  Task to check for new reviews on TA
  """
  # for obj in AspectQ.objects:
  #   obj.aspectr
  pass

