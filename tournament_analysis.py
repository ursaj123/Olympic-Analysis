import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

def heat_map(data):
    '''
    # this code is working well but not fast, so checking something without loop
    years = sorted(list(data.Year.unique()))
    sports = sorted(list(data.Sport.unique()))
    heatmap = np.zeros((len(sports), len(years)))
    for i in range(len(sports)):
        for j in range(len(years)):
            heatmap[i][j] = data[(data.Year==years[j])&(data.Sport==sports[i])].Event.nunique()
    
    fig = px.imshow(pd.DataFrame(heatmap, columns=years, index=sports), width=800, height=800, text_auto=True)
    return fig
    '''
    temp = data.loc[:, ['Year', 'Sport', 'Event']].drop_duplicates().sort_values(
    'Year').pivot_table(index='Sport', columns='Year', values='Event', 
                        aggfunc='count').fillna(0).astype('int')
    # plotly plot not looking good
    # fig = px.imshow(temp, width=1000, height=1000, text_auto=True)
    fig, axes = plt.subplots(figsize=(20, 20))
    axes = sns.heatmap(temp, annot=True)
    return fig
    # this code runs very fast (dekh kar jo likha hai)
     
def most_decorated_athlete(data, sport='Overall'):
    if sport=='Overall':
        temp = data.loc[:,['Name', 'Sport', 'NOC', 'Gold', 'Silver', 'Bronze']].groupby(['Name', 'Sport', 'NOC']).sum(
    numeric_only=True).sort_values(['Gold', 'Silver', 'Bronze'], ascending=False).head(15).reset_index('NOC'
    ).reset_index('Sport').reset_index('Name')

        return temp
    else:
        temp = data[data.Sport==sport]
        temp = temp.loc[:, ['Name', 'NOC', 'Gold', 'Silver', 'Bronze']].groupby(['Name', 'NOC']).sum().reset_index(
        'NOC').reset_index('Name').sort_values(['Gold', 'Silver', 'Bronze'], ascending=False).reset_index(0).drop(
            'index',axis=1).head(15)
        return temp
    
#def 
    