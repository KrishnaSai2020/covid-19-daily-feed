import datetime
import pandas as pd
import requests
from bokeh.models.tools import HoverTool
from bokeh.plotting import figure, output_file, save
from flask import Flask, render_template

output_file("templates/daily_death_graph.html")

app = Flask(__name__)


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


def daily_deaths():
    response = request_api_data()
    data = response['data']
    df_dict = {
        'date': [],
        'daily_deaths': []
    }

    for dictionary in data:
        timestamp = dictionary['date']
        timestamp /= 1000
        your_dt = datetime.datetime.fromtimestamp(int(timestamp))  # using the local timezone
        print(your_dt)
        deaths = dictionary['death']
        df_dict['daily_deaths'].append(deaths)
        df_dict['date'].append(your_dt)

    df1 = pd.DataFrame(df_dict, columns=['daily_deaths'])
    df2 = pd.DataFrame(df_dict, columns=['date'])

    df3 = df1.diff(1)
    result = pd.concat([df2, df3], axis=1, sort=False)
    result = result.loc[result['daily_deaths'] > 0]
    p = figure(title="Daily new deaths in the U.K", x_axis_label='date', x_axis_type='datetime', y_axis_label='Daily_deaths', plot_width=800, plot_height=600)
    p.line(source=result, x='date', y='daily_deaths')
    p.circle(source=result, x='date', y='daily_deaths', fill_color="blue", line_color="blue", size=6)

    hover_tool = HoverTool(tooltips=[
        ('daily_deaths', '@daily_deaths{000}'),

    ], formatters={
            'daily_deaths': 'numeral',
    },
        mode='vline'
    )
    p.tools.append(hover_tool)
    save(p, 'templates/daily_death_graph.html')


def daily_cases():
    res = request_api_data()
    data = res['data']
    df_dict = {
        'date': [],
        'daily_cases': []
    }

    for dictionary in data:
        timestamp = dictionary['date']
        timestamp /= 1000
        your_dt = datetime.datetime.fromtimestamp(int(timestamp))  # using the local timezone
        print(your_dt)
        cases = dictionary['confirmed']
        df_dict['daily_cases'].append(cases)
        df_dict['date'].append(your_dt)

        df1 = pd.DataFrame(df_dict, columns=['daily_cases'])
        df2 = pd.DataFrame(df_dict, columns=['date'])

        df3 = df1.diff(1)
        result = pd.concat([df2, df3], axis=1, sort=False)
        result = result.loc[result['daily_cases'] > 0]
        p = figure(title="Daily new cases in the U.K", x_axis_label='date', x_axis_type='datetime',
                   y_axis_label='Daily_cases', plot_width=800, plot_height=600)
        p.line(source=result, x='date', y='daily_cases')
        p.circle(source=result, x='date', y='daily_cases', fill_color="blue", line_color="blue", size=6)

        hover_tool = HoverTool(tooltips=[
            ('daily_cases', '@daily_cases{000}'),

        ], formatters={
            'daily_cases': 'numeral',
        },
            mode='vline'
        )
        p.tools.append(hover_tool)
        save(p, 'templates/daily_cases_graph.html')


@app.route('/')
def my_home():
    return render_template('home.html')


@app.route('/<string:page_name>')
def html_page(page_name):
    if page_name == 'daily_deaths.html':
        daily_deaths()
        return render_template('daily_deaths.html')
    if page_name == 'daily_cases.html':
        daily_cases()
        return render_template('daily_cases.html')
    else:
        return render_template(page_name)
