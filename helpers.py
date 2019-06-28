# _*_ coding: utf-8 _*_
import json


def fetchNewVersion():
    pass


def fetchCurrentVersion():
    with open("mHosts.json", mode="r") as data:
        json_data = json.load(data)
        return json_data["version"]
