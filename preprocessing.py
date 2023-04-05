import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

def preprocess(data, region_data):
    # i'm selecting only the summer olympics data
    data = data[data.Season=='Summer']
    
    # i want to map each of NOC in the data with the respective countries mentioned in region_data
    # missing values in region_data.region is gonna create problem so first of all let us replace them 
    # with the corresponding notes value
    missing_countries = pd.DataFrame(region_data[region_data.region.isnull()].iloc[:, [0,2]].values, columns=['NOC', "Country"])   
    given_countries = pd.DataFrame(region_data[region_data.region.notnull()].iloc[:, [0,1]].values, columns=['NOC', "Country"])
    NOC_to_country = pd.concat([missing_countries, given_countries], axis=0).reset_index(0).drop(['index'], axis=1)  
    # its first three terms were NaN in Country column so i just changed them with the notes column and
    # kept all other values of the countries
    
    # let us find out which are the common NOC's in both the set, then we will take only those rows
    # having proper country name and NOC and whose country names are not NAN
    # a = set(data.NOC.unique())
    # b = set(NOC_to_country.NOC.unique())
    # c = a.intersection(b)
    # print(len(a), len(b), len(c), a-c, b-c)
    # the problem is that Singapore is written by 'SGP' in data and by 'SIN' in NOC_to_country
    # so let us replace 'SIN' in NOC_to_country by 'SGP' so that no error is returned  during mapping
    NOC_to_country.at[180, 'NOC'] = 'SGP'
    
    # let us now map NOC column by their respective country names
    NOCs = list(NOC_to_country.iloc[:, 0])
    countries = list(NOC_to_country.iloc[:, 1])
    dict_ = {NOCs[i]:countries[i] for i in range(len(NOCs))}
    data.NOC = data.NOC.apply(lambda x:dict_[x])
    # dropping the unnecessary columns
    data = data.drop(['ID', 'Team', 'Season', 'Games'], axis=1).reset_index(0).drop('index', axis=1)
    
    # now first fixing out the problem of Medal column
    medals = pd.get_dummies(data.Medal, columns=['Gold', 'Silver', 'Bronze'], dtype=int).iloc[:, [1,2,0]]
    data = pd.concat([data, medals], axis=1).drop('Medal', axis=1)
    
    # let us now check if there are any duplicated rows, and if any them remove them
    data = data.drop_duplicates().reset_index(0).drop('index', axis=1)
    return data
    