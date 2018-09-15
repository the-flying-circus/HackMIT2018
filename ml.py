#!/usr/bin/env python3

import requests
from pprint import pprint

import secrets


# IBM Personality Insights API root
IBM_PI_ROOT = "https://gateway.watsonplatform.net/personality-insights/api/v3/profile"


class PersonalityService:
    def __init__(self):
        self.sess = requests.Session()
        self.sess.auth = (secrets.IBM_USER, secrets.IBM_PW)
        self.sess.headers = {
            "content-type": "text/plain",
            "accept": "application/json"
        }
        self.sess.params = {
            "version": "2017-10-13"
        }

    def get_insights(self, text: str) -> dict:
        response = self.sess.post(IBM_PI_ROOT, data=text)
        return response.json()


if __name__ == "__main__":
    text = "I am sad. " * 1000
    service = PersonalityService()
    pprint(service.get_insights(text))
