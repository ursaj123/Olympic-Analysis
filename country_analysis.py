import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

def country_medal_plot(data, country):
    temp = data[data.NOC==country].loc[:, ['Year', 'Sport','Event', 'Gold', 'Silver', 'Bronze']].sort_values('Year'
    ).drop_duplicates().groupby('Year').sum(numeric_only=True).reset_index('Year')
    temp['Total'] = temp['Gold'] + temp['Silver'] + temp['Bronze']
    fig = px.line(temp, x='Year', y=['Total', 'Gold', 'Silver', 'Bronze'])
    return fig

def best_sport(data, country):
    temp = data[data.NOC==country].loc[:, ['Year', 'Sport', 'Event', 'Gold', 'Silver', 'Bronze']].drop_duplicates(
    ).drop('Event', axis=1).groupby(['Year', 'Sport']).sum().reset_index('Year').drop('Year', axis=1
    ).groupby('Sport').sum().reset_index('Sport').sort_values(['Gold', 'Silver', 'Bronze'], ascending=False
    ).reset_index(0).drop('index', axis=1)
    fig = px.bar(temp, x='Sport', y=['Gold', 'Silver', 'Bronze'])
    return fig


def best_athletes(data, country):
    temp = data[data.NOC==country].loc[:, ['Name', 'Year', 'Sport', 'Event', 'Gold', 'Silver', 'Bronze']].drop_duplicates(
    ).groupby(['Name', 'Sport']).sum(numeric_only=True).reset_index('Sport').reset_index('Name'
    ).sort_values(['Gold', 'Silver', 'Bronze'],ascending=False).reset_index(0).drop(
        ['index', 'Year'], axis=1).head(15)
    return temp                                                                        