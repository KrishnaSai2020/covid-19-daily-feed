import requests
import hashlib
import re
from flask import Flask, render_template, request, redirect
import traceback

#app = Flask(__name__)


def request_api_data():
    url = 'https://api.covid19api.com/total/dayone/country/united-kingdom'
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'error fetching: {res.status_code}, check the api and try again ')
    return res


response = request_api_data()
data_retrieved = response.text
print(data_retrieved[-1])
