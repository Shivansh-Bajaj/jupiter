#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Survaider

from unittest.mock import MagicMock
from unittest.mock import patch

import hug
import falcon
import uuid

from jupiter.tests import BaseTestCase
from jupiter.api.directives import access_token

api = hug.API(__name__)

class TestAccessToken(BaseTestCase):
    missing_header_error = {
        'errors': {
            'Missing header value': 'The Authorization header is required.'
        }
    }

    invalid_header_error = {
        'errors': {
            'Invalid access_token': 'The supplied access token is invalid'
        }
    }

    def setUp(self):
        @hug.get()
        def access_data(token: access_token):
            return token

    def test_missing_header(self):
        self.assertEqual(
            hug.test.get(api, 'access_data').data,
            self.missing_header_error)

    def test_invalid_header(self):
        self.assertEqual(
            hug.test.get(api, 'access_data', headers={'Authorization': 'test'}).data,
            self.invalid_header_error)

    def test_valid_header(self):
        key = str(uuid.uuid4())
        with patch.dict('jupiter._config.access_tokens', {key: {'active': True}}):
            self.assertEqual(
                hug.test.get(api, 'access_data', headers={'Authorization': key}).data,
                key)

    def test_inactive_header(self):
        key = str(uuid.uuid4())
        with patch.dict('jupiter._config.access_tokens', {key: {'active': False}}):
            self.assertEqual(
                hug.test.get(api, 'access_data', headers={'Authorization': key}).data,
                self.invalid_header_error)
