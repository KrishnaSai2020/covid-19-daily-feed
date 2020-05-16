import requests


def request_api_data():
    url = 'https://api.covid19api.com/total/country/united-kingdom/status/confirmed'
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'error fetching: {res.status_code}, check the api and try again ')
    return res


response = request_api_data()
print(response.text)
