#!/usr/bin/env python3

import requests
from pprint import pprint
from typing import Tuple
import math

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

    @staticmethod
    def get_compatibility_score(insights_1: dict, insights_2: dict) -> float:
        """Lower score => more compatible."""
        sse, num_insights = PersonalityService._get_compatibility_recurse(insights_1, insights_2)
        return math.sqrt(sse / num_insights)

    @staticmethod
    def _get_compatibility_recurse(insights_1: dict, insights_2: dict) -> Tuple[float, int]:
        if type(insights_2) is dict:
            if "percentile" in insights_1:
                return (insights_1["percentile"] - insights_2["percentile"]) ** 2, 1
            results = [PersonalityService._get_compatibility_recurse(insights_1[key], insights_2[key]) for key in insights_1.keys()]
        elif type(insights_1) is list:
            results = [PersonalityService._get_compatibility_recurse(insights_1[i], insights_2[i]) for i in range(len(insights_1))]
        else:
            return 0, 0
        sse = sum(result[0] for result in results)
        num_insights = sum(result[1] for result in results)
        return sse, num_insights


if __name__ == "__main__":
    service = PersonalityService()
    results_sad = service.get_insights("I am sad. " * 1000)
    results_happy = service.get_insights("I am happy. " * 1000)
    pprint(results_sad)
    print("Compatibility scores (lower => more compatible):")
    print("  sad + sad   :", PersonalityService.get_compatibility_score(results_sad, results_sad))
    print("  sad + happy :", PersonalityService.get_compatibility_score(results_sad, results_happy))
