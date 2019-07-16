#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from urllib import parse
import json
import re
import ssl

import requests

from .ssl_helper import SSLAdapter
from .config import CONFIG, AUTH_URL_DICT

logging.basicConfig(level=logging.INFO)


class Meli:
    def __init__(self, client_id, client_secret,
                 access_token=None, refresh_token=None, auth_url_key='MXN'):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires_in = None
        self.auth_url_key = auth_url_key

        self._requests = requests.Session()
        try:
            self.SSL_VERSION = CONFIG.get('ssl_version')
            self._requests.mount(
                'https://', SSLAdapter(ssl_version=getattr(ssl,
                                                           self.SSL_VERSION)))
        except Exception as e:
            logging.warning(e)
            self._requests = requests

        self.API_ROOT_URL = CONFIG.get('api_root_url')
        self.SDK_VERSION = CONFIG.get('sdk_version')
        self.AUTH_URL = AUTH_URL_DICT.get(self.auth_url_key)
        self.OAUTH_URL = CONFIG.get('oauth_url')

    # AUTH METHODS
    def auth_url(self, redirect_URI):
        params = {'client_id': self.client_id,
                  'response_type': 'code', 'redirect_uri': redirect_URI}
        url = self.AUTH_URL + '/authorization' + '?' + parse.urlencode(params)
        return url

    def authorize(self, code, redirect_URI):
        params = {'grant_type': 'authorization_code',
                  'client_id': self.client_id,
                  'client_secret': self.client_secret,
                  'code': code, 'redirect_uri': redirect_URI}
        headers = {'Accept': 'application/json',
                   'User-Agent': self.SDK_VERSION,
                   'Content-type': 'application/json'}
        uri = self.make_path(self.OAUTH_URL)

        response = self._requests.post(uri, params=parse.urlencode(params),
                                       headers=headers)

        if response.ok:
            response_info = response.json()
            self.access_token = response_info['access_token']
            if 'refresh_token' in response_info:
                self.refresh_token = response_info['refresh_token']
            else:
                self.refresh_token = ''  # offline_access not set up
                self.expires_in = response_info['expires_in']

            return self.access_token
        else:
            # response code isn't a 200; raise an exception
            response.raise_for_status()

    def get_refresh_token(self):
        if self.refresh_token:
            params = {'grant_type': 'refresh_token',
                      'client_id': self.client_id,
                      'client_secret': self.client_secret,
                      'refresh_token': self.refresh_token}
            headers = {'Accept': 'application/json',
                       'User-Agent': self.SDK_VERSION,
                       'Content-type': 'application/json'}
            uri = self.make_path(self.OAUTH_URL)

            response = self._requests.post(uri, params=parse.urlencode(
                params), headers=headers, data=params)

            if response.ok:
                response_info = response.json()
                self.access_token = response_info['access_token']
                self.refresh_token = response_info['refresh_token']
                self.expires_in = response_info['expires_in']
                return self.access_token
            else:
                # response code isn't a 200; raise an exception
                response.raise_for_status()
        else:
            raise Exception("Offline-Access is not allowed.")

    # REQUEST METHODS
    def get(self, path, params=None, extra_headers=None, **kwargs):
        params = params or {}
        headers = {'Accept': 'application/json',
                   'User-Agent': self.SDK_VERSION,
                   'Content-type': 'application/json'}
        if extra_headers:
            headers.update(extra_headers)
        uri = self.make_path(path)
        response = self._requests.get(uri, params=parse.urlencode(params),
                                      headers=headers, **kwargs)
        return response

    def post(self, path, body=None, params=None, extra_headers=None, **kwargs):
        params = params or {}
        headers = {'Accept': 'application/json',
                   'User-Agent': self.SDK_VERSION,
                   'Content-type': 'application/json'}
        if extra_headers:
            headers.update(extra_headers)
        uri = self.make_path(path)
        if body:
            body = json.dumps(body)

        response = self._requests.post(
            uri, data=body, params=parse.urlencode(params), headers=headers,
            **kwargs)
        return response

    def put(self, path, body=None, params=None, extra_headers=None, **kwargs):
        params = params or {}
        headers = {'Accept': 'application/json',
                   'User-Agent': self.SDK_VERSION,
                   'Content-type': 'application/json'}
        if extra_headers:
            headers.update(extra_headers)
        uri = self.make_path(path)
        if body:
            body = json.dumps(body)

        response = self._requests.put(
            uri, data=body, params=parse.urlencode(params), headers=headers,
            **kwargs)
        return response

    def delete(self, path, params=None, extra_headers=None, **kwargs):
        params = params or {}
        headers = {'Accept': 'application/json',
                   'User-Agent': self.SDK_VERSION,
                   'Content-type': 'application/json'}
        if extra_headers:
            headers.update(extra_headers)
        uri = self.make_path(path)
        response = self._requests.delete(uri, params=params, headers=headers,
                                         **kwargs)
        return response

    def options(self, path, params=None, extra_headers=None, **kwargs):
        params = params or {}
        headers = {'Accept': 'application/json',
                   'User-Agent': self.SDK_VERSION,
                   'Content-type': 'application/json'}
        if extra_headers:
            headers.update(extra_headers)
        uri = self.make_path(path)
        response = self._requests.options(uri, params=parse.urlencode(params),
                                          headers=headers, **kwargs)
        return response

    def make_path(self, path, params=None):
        params = params or {}
        # Making Path and add a leading / if not exist
        if not (re.search("^\/", path)):
            path = "/" + path
        path = self.API_ROOT_URL + path
        if params:
            path = path + "?" + parse.urlencode(params)

        return path
