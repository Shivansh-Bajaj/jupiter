#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Survaider
"""Jupiter Task Runner - WebHooks API Interface

See module documentation for further information.
"""
import hug

from jupiter._config import version
from jupiter.webhooks.scopes import scope_values
from jupiter.api.directives import access_token

@hug.put('/', versions=version)
def put_hook(access_token,
      scope: hug.types.one_of(scope_values),
      callback_uri: hug.types.text):
  """Add an explicit subscription for the task completion

  Params:
    - scope: One of the valid webhook scopes
    - callback_uri: This is the URI the webhook callback will be requested
  """
  pass


delete_hook_methods = ['hook_id', 'callback_uri']

@hug.delete('/', versions=version)
def delete_hook(access_token,
      by: hug.types.one_of(delete_hook_methods),
      data: hug.types.text):
  """Remove a webhook subscription

  Params:
    - by: Specify *how* do you want to find and delete the webhook subscription
          The valid values are `hook_id`, and `callback_uri`
    - data (str): provide a valid `hook_id` or `callback_uri` as relevant
  """
  pass
