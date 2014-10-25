#!/usr/bin/env python

from __future__ import print_function
import requests
import os
import json
import pprint
import uritemplate

#quick and dirty API client for the hp publishing platform APIs
api_username = os.environ.get('HP_API_USER')
api_key = os.environ.get('HP_API_KEY')

class HpApiClient(object):
    def __init__(self):
        self.username = api_username
        self.key = api_key
        
class PublicationsClient(HpApiClient):
    def __init__(self):
        super(PublicationsClient,self ).__init__()
        self.root_url = 'https://vrapi.kraken-efd.cloudpublish.com/vrapi'
        self.base_headers = { 'api-auth-token': api_key, 'Content-Type': 'application/json' }

    def get(self):
        response = requests.get( self.root_url + '/publications', headers=self.base_headers)
        if response.status_code != 200:
            print("error %s" % response.status_code)
        else:
            return response.json()


class MarketingClient(HpApiClient):
    def __init__(self):
        super(MarketingClient,self).__init__()
        self.root_url = 'https://arion-efd.cloudpublish.com/cpapi'
        self.base_headers = { 'api-auth-token': api_key, 'Content-Type': 'application/json' }

    def get(self):
        response = requests.get( self.root_url + '/catalogviews', headers=self.base_headers )
        if response.status_code != 200:
            print("error %s" % response.status_code)
        else:
            return response.json()

class MailboxClient(HpApiClient):
    def __init__(self):
        super(MailboxClient,self).__init__()
        self.root_url = 'https://spokane-efd.cloudpublish.com/'
        self.base_headers = { 'X-API-KEY': self.key, 'Content-Type': 'application/json'}
        self.mbs = self.get()

    def get(self):
        response = requests.get( self.root_url + 'mbs', headers=self.base_headers )
        if response.status_code != 200:
            print("error %s" % response.status_code)
        else:
            return response.json()

    def permissions(self):
        response = requests.get( self.root_url + 'mbs/permissions',
                                 headers=self.base_headers )
        if response.status_code != 200:
            print("error %s" % response.status_code)
        else:
            return response.json()

if __name__=='__main__':
    pubs = PublicationsClient()
    print(pubs.root_url)
    pprint.pprint(pubs.get())

    market = MarketingClient()
    print(market.root_url)
    print(market.base_headers)
    pprint.pprint(market.get())

    mbs = MailboxClient()
    print(mbs.root_url)
    print(mbs.base_headers)
    pprint.pprint(mbs.get())

