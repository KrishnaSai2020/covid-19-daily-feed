import requests
import pandas as pd
import matplotlib.pyplot as plt
import datetime


def request_api_data():
    url = 'https://api.covid19uk.live/historyfigures'
    res = requests.get(url)
    try:
        if res.status_code != 200:
            raise RuntimeError(f'error fetching: {res.status_code}, check the api and try again ')
    except RuntimeError:
        print(f'error fetching: {res.status_code}, check the api and try again ')

    response = res.json()
    return response


response = request_api_data()
data = response['data']

df_dict = {
    'date': [],
    'daily deaths': []
}

for dict in data:
    timestamp = str(dict['date'])
    your_dt = datetime.datetime.fromtimestamp(int(timestamp) / 1000)  # using the local timezone
    date = your_dt.strftime("%m %d")
    deaths = dict['death']
    df_dict['daily deaths'].append(deaths)
    df_dict['date'].append(date)

df3 = pd.DataFrame(df_dict, columns=['daily deaths'])
df4 = pd.DataFrame(df_dict, columns=['date'])

df5 = df3.diff(1)
result = pd.concat([df4, df5], axis=1, sort=False)
result = result.loc[result['daily deaths'] > 0]

result.plot(x ='date', y='daily deaths', kind = 'bar')
plt.show()
