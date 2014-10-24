#!/usr/bin/env python

from __future__ import print_function
import requests
import os
import json


#quick and dirty API client for the hp publishing platform APIs
api_username = os.environ.get('HP_API_USER')
api_key = os.environ.get('HP_API_KEY')

root_url = 'https://vrapi.kraken-dev-36.cloudpublish.com/vrapi/'

base_headers = { 'X-API-KEY': api_key, 'Content-Type': 'application/json' }

def get_mailbox_service():
    response = requests.get( root_url + 'mbs', headers=base_headers)
    if response.status_code != 200:
        print("error %s" % response.status_code)
    else:
        print(response.text)


if __name__=='__main__':
    print(api_username)
    print(api_key)
    get_mailbox_service()
