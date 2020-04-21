#!/usr/bin/env python
# coding: utf-8

# # VacationPy
# ----
# 
# #### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[12]:


# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import gmaps
import os

# Import API key
from api_keys import g_key


# ### Store Part I results into DataFrame
# * Load the csv exported in Part I to a DataFrame

# In[13]:


g_key


# In[14]:


df1 = pd.read_csv('../output_data/cities.csv')


# ### Humidity Heatmap
# * Configure gmaps.
# * Use the Lat and Lng as locations and Humidity as the weight.
# * Add Heatmap layer to map.

# In[15]:


gmaps.configure(api_key=g_key)


# In[16]:


locations = df1[["Lat", "Lng"]]
humidity = df1["Humidity"]

fig1 = gmaps.Map()

heat = gmaps.heatmap_layer(locations, weights=humidity)
fig1.add_layer(heat)


# ### Create new DataFrame fitting weather criteria
# * Narrow down the cities to fit weather conditions.
# * Drop any rows will null values.

# In[17]:


idf = df1.loc[df1['Max Temp'] < 80, :]
idf = idf.loc[idf['Max Temp'] > 70, :]
idf = idf.loc[idf['Wind Speed'] < 10, :]
idf = idf.loc[idf['Cloudiness'] == 0, :]


# ### Hotel Map
# * Store into variable named `hotel_df`.
# * Add a "Hotel Name" column to the DataFrame.
# * Set parameters to search for hotels with 5000 meters.
# * Hit the Google Places API for each city's coordinates.
# * Store the first Hotel result into the DataFrame.
# * Plot markers on top of the heatmap.

# In[21]:


hotel_df = idf
hotel_df['Hotel Name'] = np.nan

param1 = "Hotel"
param2 = 5000
param3 = "lodging"

counter = 0
for index, row in hotel_df.iterrows():
    params = {
        "location": f"{row['Lat']}, {row['Lng']}",
        "keyword": param1,
        "radius": param2,
        "type": param3,
        "key": g_key
    }

    base = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    response = requests.get(base, params=params)
    response_json = response.json()
    results = response_json['results']
    if len(results) > 0:
        name = response_json['results'][0]['name']
        hotel_df.iloc[idx, -1] = name
    counter = counter + 1

narrowed_city_df = hotel_df


# In[22]:


# NOTE: Do not change any of the code in this cell

# Using the template add the hotel marks to the heatmap
info_box_template = """
<dl>
<dt>Name</dt><dd>{Hotel Name}</dd>
<dt>City</dt><dd>{City}</dd>
<dt>Country</dt><dd>{Country}</dd>
</dl>
"""
# Store the DataFrame Row
# NOTE: be sure to update with your DataFrame name
hotel_info = [info_box_template.format(**row) for index, row in narrowed_city_df.iterrows()]
locations = hotel_df[["Lat", "Lng"]]


# In[23]:


# Add marker layer ontop of heat map

layer = gmaps.marker_layer(locations, info_box_content=hotel_info)
fig1.add_layer(layer)

# Display Map
fig1


# In[ ]:





# In[ ]:




