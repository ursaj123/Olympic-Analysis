# importing the required libraries
import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
# importing functions from the files
import preprocessing
import medal_tally
import tournament_analysis
import country_analysis
import player_analysis


# importing the datasets
athlete_data = pd.read_csv('athlete_events.csv')
region_data = pd.read_csv('noc_regions.csv')

# preprocessing the datasets
data = preprocessing.preprocess(athlete_data, region_data)

# first of all making a sidebar for options to select 
st.sidebar.image('logo.png')
sidebar = st.sidebar.radio(
    "Select an option", 
    ("Medal Tally", "Tournament  Analysis", "Country-wise-analysis", "Player-wise-analysis")
)


if sidebar=='Medal Tally':
    # list of all countries
    countries_list = ['Overall'] + sorted(list(set(data.NOC)))
    # list of years in which olympic was played
    years_list = ['Overall'] + sorted(list(set(data.Year)))   
    
    country = st.sidebar.selectbox('Select a country', countries_list)
    year = st.sidebar.selectbox('Select a Year', years_list)
    
    if country=='Overall' and year=='Overall':
        st.title('Overall Medal Tally')
    elif country!='Overall' and year=='Overall':
        st.title(country + "'s performance over the years")
    elif country=='Overall' and year!='Overall':
        st.title(str(year) + ' medal tally')
    else:
        st.title(country + "'s performance in " + str(year))
    st.table(medal_tally.get_medal_tally(data, country, year))
    
    
elif sidebar=='Tournament  Analysis':
    st.title('Top Statistics')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.subheader(data.Year.nunique())
    with col2:
        st.header('Host Cities')
        st.subheader(data.City.nunique())
    with col3:
        st.header('Countries')
        st.subheader(data.NOC.nunique())
        
    col4, col5, col6 = st.columns(3)
    with col4:
        st.header('Sports')
        st.subheader(data.Sport.nunique())
    with col5:
        st.header('Events')
        st.subheader(data.Event.nunique())
    with col6:
        st.header('Athletes')
        st.subheader(data.Name.nunique())
        
    # now let us plot some graphs
    st.title('Number of Nations participating over the years')
    temp = data.groupby('Year').nunique().reset_index('Year').sort_values('Year').loc[:, ['Year', 'NOC']]
    temp = temp.rename({'NOC':'Number of Participating Countries'}, axis=1)
    fig = px.line(data_frame=temp, x='Year', y='Number of Participating Countries', markers=True)
    st.plotly_chart(fig)
    
    st.title('Number of Events over the years')
    temp = data.groupby('Year').nunique().reset_index('Year').sort_values('Year').loc[:, ['Year', 'Event']]
    temp = temp.rename({'Event':'Number of Events'}, axis=1)
    fig = px.line(data_frame=temp, x='Year', y='Number of Events', markers=True)
    st.plotly_chart(fig)
    
    st.title("Number of Athletes over the years")
    temp = data.groupby('Year').nunique().reset_index('Year').sort_values('Year').loc[:, ['Year', 'Name']]
    temp = temp.rename({'Name':'Number of Athletes'}, axis=1)
    fig = px.line(data_frame=temp, x='Year', y='Number of Athletes', markers=True)
    st.plotly_chart(fig)
    
    st.title('Number of events in each sports (all years)')
    #st.plotly_chart(tournament_analysis.heat_map(data))
    # st.pyplot(tournament_analysis.heat_map(data))
    # could have done the above line, but it takes time to load
    # everytime and it is a static image thus i have downloaded it
    # and just displaying it as a image
    st.image('temp.png')
    
    st.title('Most Decorated Athletes (Sport-wise)')
    sport = st.selectbox('Select a Sport', options=['Overall'] + 
                sorted(list(data.Sport.unique())))
    st.table(tournament_analysis.most_decorated_athlete(data, sport))
    
    
    
elif sidebar=="Country-wise-analysis":
    st.title('Country-wise analysis')
    country = st.selectbox('Select a country', sorted(list(data.NOC.unique())))
    #col1, col2 = st.columns(2)
    #with col1:
    st.header('Country-Medal plot')
    st.plotly_chart(country_analysis.country_medal_plot(data, country))
    #with col2:
    st.header('Best Sports for '+ country+' in Olympics')
    st.plotly_chart(country_analysis.best_sport(data, country))
    st.header('Best athletes for '+country+' in Olympics')
    st.table(country_analysis.best_athletes(data, country))
    
else:
    st.title('Age vs Medal Distribution')
    st.plotly_chart(player_analysis.age_medal(data))
    
    st.title('Age vs Sport distribution (Gold Medalist Only)')
    st.plotly_chart(player_analysis.age_distrib(data))
    
    sport = st.selectbox('Select a Sport', sorted(list(data.Sport.unique())))
    st.pyplot(player_analysis.weight_height(data, sport))
    
    st.title('Male vs Female Participation')
    st.plotly_chart(player_analysis.men_women(data))
    
    
    
    
    
    
    