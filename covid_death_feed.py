import requests
import matplotlib.pyplot as plt
import datetime
from flask import Flask, render_template, request, redirect
import pandas as pd
from bokeh.plotting import figure, output_file, save, show
from bokeh.models.tools import HoverTool
from bokeh.resources import CDN
from bokeh.embed import autoload_static, server_document

output_file("templates/daily_death_graph.html")


app = Flask(__name__)


def request_api_data1():
    url = 'https://api.covid19uk.live/historyfigures'
    res = requests.get(url)
    try:
        if res.status_code != 200:
            raise RuntimeError(f'error fetching: {res.status_code}, check the api and try again ')
    except RuntimeError:
        print(f'error fetching: {res.status_code}, check the api and try again ')

    response = res.json()
    return response


def daily_deaths():
    response = request_api_data1()
    data = response['data']
    df_dict = {
        'date': [],
        'daily_deaths': []
    }

    for dict in data:
        timestamp = str(dict['date'])
        your_dt = datetime.datetime.fromtimestamp(int(timestamp) / 1000)
        date = your_dt
        deaths = dict['death']
        df_dict['daily_deaths'].append(deaths)
        df_dict['date'].append(date)

    df1 = pd.DataFrame(df_dict, columns=['daily_deaths'])
    df2 = pd.DataFrame(df_dict, columns=['date'])

    df3 = df1.diff(1)
    result = pd.concat([df2, df3], axis=1, sort=False)
    result = result.loc[result['daily_deaths'] > 0]

    p = figure(title="simple line example", x_axis_label='date',x_axis_type='datetime', y_axis_label='Daily_deaths',plot_width=400,plot_height=400)
    p.line(source=result, x='date',y='daily_deaths')
    save(p, 'templates/daily_death_graph.html')
    # js, tag = autoload_static(p, CDN, "static/daily_death_grap_plot.js")


@app.route('/')
def my_home():
    return render_template('home.html')


@app.route('/<string:page_name>')
def html_page(page_name):
    if page_name == 'daily_deaths.html':
        tag = daily_deaths()
        return render_template('daily_deaths.html')
    else:
        return render_template(page_name)


# def request_api_data():
#     url = 'https://api.covid19uk.live/historyfigures'
#     res = requests.get(url)
#     try:
#         if res.status_code != 200:
#             raise RuntimeError(f'error fetching: {res.status_code}, check the api and try again ')
#     except RuntimeError:
#         print(f'error fetching: {res.status_code}, check the api and try again ')
#
#     response = res.json()
#     return response
#
#
# response = request_api_data()
# data = response['data']
# df_dict = {
#     'date': [],
#     'daily deaths': []
# }
#
# for dict in data:
#     timestamp = str(dict['date'])
#     your_dt = datetime.datetime.fromtimestamp(int(timestamp) / 1000)
#     date = your_dt.strftime("%m %d")
#     deaths = dict['death']
#     df_dict['daily deaths'].append(deaths)
#     df_dict['date'].append(date)
#
# df3 = pd.DataFrame(df_dict, columns=['daily deaths'])
# df4 = pd.DataFrame(df_dict, columns=['date'])
#
# df5 = df3.diff(1)
# result = pd.concat([df4, df5], axis=1, sort=False)
# result = result.loc[result['daily deaths'] > 0]
#
# result.plot(x='date', y='daily deaths', kind='bar')
# plt.show()
