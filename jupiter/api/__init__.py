#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Survaider

"""Jupiter Task Runner API Base Interface

This module exists with following simple goals:
- Manage tasks with a set of credentials into the periodic task runners.
    - Credentials are the Zomato/Tripadvisor/etc., IDs and other information
      that are sufficient to perform the aggregation tasks and any other stuff.
- Management provides the following interfaces via REST Endpoints:
    - Add a credential
    - Get the status
    - Revoke/Delete the task
- The API also provides an interface to subscribe to server webhooks which
  are sent to the requesting server when the tasks are completed.
    - Add a webhook subscription
    - Remove the subscription
"""
