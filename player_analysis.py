import numpy as np
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import seaborn as sns
import matplotlib.pyplot as plt

def age_medal(data):
    #temp = data.loc[:, ['Name', 'Age', 'Event', 'Gold', 'Silver', 'Bronze']].drop_duplicates()#groupby('Year')
    #temp = temp.groupby(['Name', 'Age']).sum(numeric_only=True).reset_index('Name').sort_values('Gold', 
    #ascending=False).reset_index('Age').drop('Name', axis=1).groupby('Age').sum().reset_index('Age').sort_values('Age')
    #x1 = temp.Age
    #x2 = temp.Gold
    #x3 = temp.Silver
    #x4 = temp.Bronze
    #fig = ff.create_distplot([x1,x2,x3,x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 
                                         #'Bronze Medalist'], show_hist=True, show_rug=False)
    #fig = px.histogram(temp, x='Age', y=['Gold', 'Silver', 'Bronze'])
                                         
    temp = data.drop_duplicates(subset=['Name', 'NOC'])
    x1 = temp['Age'].dropna()
    x2 = temp[temp.Gold!=0]['Age'].dropna()
    x3 = temp[temp.Silver!=0]['Age'].dropna()
    x4 = temp[temp.Bronze!=0]['Age'].dropna()
    fig = ff.create_distplot([x1,x2,x3,x4], ['Overall', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'
                                        ], show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=800, height=600)
    return fig


def age_distrib(data):
    temp = data.drop_duplicates(subset=['Name', 'NOC'])
    famous_sports = []
    all_sports = list(data.Sport.unique())
    for sport in all_sports:
        if len(temp[temp.Sport==sport])>1500:
            famous_sports.append(sport)
    x = []
    name = []
    for sport in famous_sports:
        temp_df = temp[temp.Sport==sport]
        x.append(temp_df[temp_df.Gold!=0].Age.dropna())
        name.append(sport)
    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=800, height=600)
    return fig
 
def func(row):
    if row.Gold!=0:
        return 'Gold'
    elif row.Silver!=0:
        return 'Silver'
    elif row.Bronze!=0:
        return 'Bronze'
    else:
        return 'No Medal'       
    
def weight_height(data, sport):
    temp = data.drop_duplicates(subset=['Name', 'NOC'])
    temp['Medal'] = temp.apply(lambda x:func(x), axis=1)
    temp = temp[temp.Sport==sport].dropna()
    fig, axes = plt.subplots()
    axes = sns.scatterplot(x = temp['Weight'], y = temp['Height'], hue=temp['Medal'], style=temp['Sex'], s=100)
    return fig


def men_women(data):
    temp = data.drop_duplicates(subset=['Name', 'NOC'])
    men = temp[temp.Sex=="M"].groupby('Year').count()['Name'].reset_index()
    women = temp[temp.Sex=="F"].groupby('Year').count()['Name'].reset_index()
    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x':'Male', 'Name_y':'Female'}, inplace=True)
    final.fillna(0, inplace=True)
    fig = px.line(final, x='Year', y=['Male', 'Female'])
    return fig
    
    
    
    
    
    
    
    