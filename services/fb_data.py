#!/usr/bin/env python3

import requests
from flask_login import current_user

import secrets


# FB user Graph API endpoint
FB_USER_ROOT = "https://graph.facebook.com/v3.1/"


class FBService:
    def __init__(self):
        self.sess = requests.Session()

    def get_user_info(self, user):
        user_id = user.social_id
        params = {
            "access_token": user.access_token
        }
        response = self.sess.get("{}{}/feed".format(FB_USER_ROOT, user_id), params=params)
        return response.json()
