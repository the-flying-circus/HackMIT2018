import requests
from flask_login import current_user
from datetime import datetime

from . import secrets


# FB user Graph API endpoint
FB_USER_ROOT = "https://graph.facebook.com/v3.1/"

class FBService:
    def __init__(self):
        self.sess = requests.Session()

    def get_user_posts(self, user):
        user_id = user.social_id
        params = {
            "access_token": user.access_token
        }
        response = self.sess.get("{}{}/feed".format(FB_USER_ROOT, user_id), params=params)
        posts = response.json()["data"]
        reformatted_posts = {"contentItems": []}
        for post in posts:
            if "message" in post:
                created_time = datetime.strptime(post["created_time"], "%Y-%m-%dT%H:%M:%S%z")
                reformatted_posts["contentItems"].append({
                    "content": post["message"],
                    "contenttype": "text/plain",
                    "created": int(created_time.timestamp() * 1000),
                    "language": "en"
                })
        return reformatted_posts
