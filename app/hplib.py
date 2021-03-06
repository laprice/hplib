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
    """
    Handles Creation and access to Mailboxes.
    Responsible for creating mailboxes.
    Responsible for Looking for Mailboxes for a given user.
    """
    def __init__(self):
        super(MailboxClient,self).__init__()
        self.root_url = 'https://spokane-efd.cloudpublish.com/mbs'
        self.base_headers = { 'X-API-KEY': self.key, 'Content-Type': 'application/json'}
        self.mbs = self.get(self.root_url)
        self.mailboxes = {}

    def get(self, url):
        response = requests.get( url, headers=self.base_headers )
        if response.status_code != 200:
            print("error %s" % response.status_code)
        else:
            return response.json()

    def permissions(self):
        return self.get( self.mbs['permissionsUrl'])

    def create_mailbox(self, userspec):
        url = uritemplate.expand(self.mbs['mailboxUsersUrlTemplate'], userspec)
        response = requests.post( url,
                                  headers=self.base_headers,
                                  json=userspec)
        if response.status_code == 201:
            self.mailboxes[userspec['userId']] = response.json()
            return response.json()
        elif response.status_code == 400:
            if not self.mailboxes.has_key(userspec['userId']):
                self.mailboxes[userspec['userId']] = requests.get(url, headers=self.base_headers).json()
        return self.mailboxes[userspec['userId']]

    def user_url(self, userspec):
        return uritemplate.expand(self.mbs['mailboxUsersUrlTemplate'], userspec)

    def get_user_mailbox(self, userspec):
        return requests.get(self.user_url(userspec), headers=self.base_headers).json()

    def get_user_items(self, userspec):
        url = self.mailboxes[userspec['userId']]['itemsUrl']
        return requests.get(url, self.base_headers).json()

    def add_user_item(self, userspec, item):
        """
        item = {
        "title": "Cycling Today, May Edition",
        "contentUrl": "http://cyclingtoday.com/2014/04.pdf",
        "senderName", "Cycling Today"
        }
        """
        url = self.mailboxes[userspec['userId']]['itemsUrl']
        response = requests.post(self.user_url(userspec),
                                 headers=self.base_headers,
                                 json=item)
        if response.status_code != 201:
            print("error adding item %s" % response.status_code)
        else:
            return response.json()

    def add_user_gcp(self, userspec, return_url):
        pass
    
    def deliver_to_mailbox(self, userspec, filename):
        pass


if __name__=='__main__':
    # pubs = PublicationsClient()
    # print(pubs.root_url)
    # pprint.pprint(pubs.get())

    # market = MarketingClient()
    # print(market.root_url)
    # print(market.base_headers)
    # pprint.pprint(market.get())
    
    mbs = MailboxClient()
    print(mbs.root_url)
    print(mbs.base_headers)
    pprint.pprint(mbs.mbs)
    pprint.pprint(mbs.permissions())
    userspec = { 'userId': 'hpux@example.com', 'userDomain': 'lurch'}
    pprint.pprint(mbs.create_mailbox(userspec))
    pprint.pprint(mbs.get_user_mailbox(userspec))
    pprint.pprint(mbs.get_user_items(userspec))
