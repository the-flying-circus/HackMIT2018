import requests
from pprint import pprint
from typing import Tuple
import math

from . import secrets


# IBM Personality Insights API root
IBM_PI_ROOT = "https://gateway.watsonplatform.net/personality-insights/api/v3/profile"


class PersonalityService:
    def __init__(self):
        self.sess = requests.Session()
        self.sess.auth = (secrets.IBM_USER, secrets.IBM_PW)
        self.sess.headers = {
            "accept": "application/json"
        }
        self.sess.params = {
            "version": "2017-10-13"
        }

    def get_personality(self, data) -> dict:
        if type(data) is str:
            self.sess.headers["content-type"] = "text/plain"
            response = self.sess.post(IBM_PI_ROOT, data=data)
        else:
            self.sess.headers["content-type"] = "application/json"
            response = self.sess.post(IBM_PI_ROOT, json=data)
        insights = response.json()
        return {trait["name"].lower().replace(' ', '_'): trait["percentile"] for trait in insights["personality"]}

    @staticmethod
    def get_compatibility_score(personality_1: dict, personality_2: dict) -> float:
        """Lower score => more compatible."""
        sse = sum((personality_1[trait] - personality_2[trait]) ** 2 for trait in personality_1)
        return math.sqrt(sse / len(personality_1))


if __name__ == "__main__":
    service = PersonalityService()
    results_sad = service.get_personality("I am sad. " * 1000)
    results_happy = service.get_personality("I am happy. " * 1000)
    pprint(results_sad)
    print("Compatibility scores (lower => more compatible):")
    print("  sad + sad   :", PersonalityService.get_compatibility_score(results_sad, results_sad))
    print("  sad + happy :", PersonalityService.get_compatibility_score(results_sad, results_happy))
