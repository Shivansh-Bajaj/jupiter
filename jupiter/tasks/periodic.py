#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Survaider
from huey import crontab

from jupiter import huey


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
  from here. It is important to note that these tasks are **required** to be
  non-blocking and must be huey tasks.

  To prevent any magic to happen, do **not** spawn any periodic tasks inside.
  """
  pass

@huey.periodic_task(crontab(minute='*/15'))
def spawn_processor_m_15():
  """These processors are run every 15 minutes

  Processors Index
  ----------------
  These processors are explicitly run:
  - (Extend this list as needed)
  """
  pass
