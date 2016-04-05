#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Survaider
"""Jupiter Task Runner - Directives

This is a utility module -- meaning, it isn't an API enpoint.
This provides a credential management interface so only valid requests are
accepted.
"""
import hug
import falcon

from jupiter._config import access_tokens

@hug.directive()
def access_token(request, **kwa):
  """Check API Keys and Verify them"""
  api_key = request.get_header('Authorization')
  if not api_key:
    raise falcon.HTTPMissingHeader(header_name='Authorization')

  if not api_key in access_tokens or not access_tokens[api_key]['active']:
    raise falcon.HTTPForbidden(
      title='Invalid access_token',
      description='The supplied access token is invalid'
    )

  return api_key
