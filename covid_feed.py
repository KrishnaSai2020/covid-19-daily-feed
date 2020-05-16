import requests
import pandas as pd


def request_api_data():
    url = 'https://api.covid19api.com/total/country/united-kingdom/status/confirmed'
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'error fetching: {res.status_code}, check the api and try again ')
    response = res.json()
    return response


response = request_api_data()
dict_of_case_nums = {
    'date' : [],
    'cases' : []
}
for dict in response:
    dict_of_case_nums['cases'].append(dict['Cases'])
    dict_of_case_nums['date'].append(dict['Date'])

df = pd.DataFrame(dict_of_case_nums, columns=['date', 'cases'])
print(df)
