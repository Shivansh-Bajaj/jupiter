#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Survaider

"""Jupiter Task Runner - WebHooks API Interface

See module documentation for further information.
"""

import hug
import falcon
from mongoengine import ValidationError, NotUniqueError

from jupiter._config import version
from jupiter.api.directives import access_token
from jupiter.webhooks.model import Hook, scope_values


@hug.put('/', versions=version)
def put_hook(key: access_token,
            scope: hug.types.one_of(scope_values),
            callback_uri: hug.types.text):
    """Add an explicit subscription for the task completion

    Params:
    - scope: One of the valid webhook scopes
    - callback_uri: This is the URI the webhook callback will be requested
    """
    try:
        hook = Hook()
        hook.scope = scope
        hook.callback = callback_uri
        hook.save()

        return hook.repr
    except ValidationError:
        raise falcon.HTTPBadRequest(
            title='ValidationError',
            description='The parameters provided are invalid')

    except NotUniqueError:
        raise falcon.HTTPBadRequest(
            title='NotUniqueError',
            description='The given scope - callback combination is taken')

delete_hook_methods = ['hook_id', 'callback_uri']

@hug.delete('/', versions=version)
def delete_hook(key: access_token,
                by: hug.types.one_of(delete_hook_methods),
                dat: hug.types.text):
    """Remove a webhook subscription

    Params:
    - by: Specify *how* do you want to find and delete the webhook subscription
          The valid values are `hook_id`, and `callback_uri`
    - dat (str): provide a valid `hook_id` or `callback_uri` as relevant
    """
    try:
        if by == 'hook_id':
            hook = Hook.objects(id=dat)
        elif by == 'callback_uri':
            hook = Hook.objects(callback=dat)
        else:
            raise ValueError

        deletes = []
        for hook_ob in hook:
            deletes.append(hook_ob.repr)
            hook_ob.delete()

        return {
            'action': 'Delete',
            'hooks': deletes
        }

    except ValueError:
        raise falcon.HTTPBadRequest(
            title='ValueError',
            description='`by` contains unsupported value')
