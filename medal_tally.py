import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

def get_medal_tally(data, country='Overall', year='Overall'):
    event_specific_data = data.iloc[:, 5:].drop_duplicates()
    
    if country=='Overall' and year=='Overall':
        overall_medal_tally = event_specific_data.groupby('NOC').sum(numeric_only=True).sort_values(
            ['Gold', 'Silver', 'Bronze'], ascending=False).reset_index('NOC').drop('Year', axis=1)   
        # creating a Total column also
        overall_medal_tally['Total'] = (overall_medal_tally['Gold'] + overall_medal_tally['Silver'] 
                                        + overall_medal_tally['Bronze'])
        return overall_medal_tally.set_index('NOC')
    
    
    
    elif country!='Overall' and year=='Overall':
        country_medal_tally = event_specific_data[event_specific_data.NOC==country].drop('NOC',
        axis=1).sort_values('Year').groupby('Year').sum(numeric_only=True).reset_index('Year')
        
        country_medal_tally['Total'] = (country_medal_tally['Gold'] + country_medal_tally['Silver'] 
                                        + country_medal_tally['Bronze'])
        return country_medal_tally.set_index('Year')
    
    
    elif country=='Overall' and year!='Overall':
        year_medal_tally = event_specific_data[event_specific_data.Year==year].drop('Year', axis=1
        ).groupby('NOC').sum(numeric_only=True).reset_index('NOC').sort_values(['Gold', 'Silver', 'Bronze']
        , ascending=False).reset_index(0).drop('index', axis=1)
        
        year_medal_tally['Total'] = (year_medal_tally['Gold'] + year_medal_tally['Silver'] 
                                        + year_medal_tally['Bronze'])
        return year_medal_tally.set_index('NOC')
        
    else:
        tally = data[(data.NOC==country) & (data.Year==year)].iloc[:, [0,8,9,10,11,12]].sort_values(
            ['Gold', 'Silver', 'Bronze'], ascending=False).reset_index(0).drop('index', axis=1)
        return tally.set_index('Name')
    


