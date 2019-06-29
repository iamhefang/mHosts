# _*_ coding: utf-8 _*_
import json
import os


def FetchNewVersion():
    pass


def FetchCurrentVersion():
    with open("mHosts.json", mode="r") as data:
        json_data = json.load(data)
        return json_data["version"]


def HasPermission(path):
    return os.access(path, os.R_OK | os.W_OK)


def ReadText(file, encoding="utf-8"):
    with open(file, mode="r", encoding=encoding) as file:
        return "".join(file.readlines())
