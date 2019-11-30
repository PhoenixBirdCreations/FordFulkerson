# -*- coding: utf-8 -*-
"""
description here...
"""

#%% Import data from JSON file
import json
with open('indianaPipelines1988.json', 'r') as json_file:
    data = json.load(json_file) # data is a dictionary
pipelines = data['features']    # list of dictionaries
#%%

#%% Build a dataframe of vertices
import pandas as pd
vertices = pd.DataFrame(columns=['lon', 'lat'])
for pipe in pipelines:
    if ((pipe['attributes']['PIPE_TYPE']=='Crude Oil') & 
        (pipe['attributes']['PIPE_CLASS']=='Intrastate')):
        node_list = pipe['geometry']['paths'][0]
        for node in node_list:
            entry = pd.DataFrame({'lon': node[0], 'lat': node[1]}, index=[0])
            vertices = vertices.append(entry, ignore_index=True)        
vertices.drop_duplicates(keep='first', inplace=True)
vertices.reset_index(inplace=True)
vertices.drop(columns=['index'], inplace=True)
#%%

#%% Build a dataframe of directed edges
edges = pd.DataFrame(columns=['id1', 'id2', 'size'])
for pipe in pipelines:
    if ((pipe['attributes']['PIPE_TYPE']=='Crude Oil') & 
        (pipe['attributes']['PIPE_CLASS']=='Intrastate')):
        node_list = pipe['geometry']['paths'][0]
        for i in range(len(node_list)-1):
            cord_node1 = node_list[i]
            cord_node2 = node_list[i+1]
            id1 = vertices.loc[(vertices['lon']==cord_node1[0]) & 
                               (vertices['lat']==cord_node1[1])].index[0]
            id2 = vertices.loc[(vertices['lon']==cord_node2[0]) & 
                               (vertices['lat']==cord_node2[1])].index[0]
            size = int(pipe['attributes']['PIPE_SIZE'])
            entry = pd.DataFrame({'id1':id1, 'id2':id2, 'size':size}, 
                                 index=[0])
            edges = edges.append(entry, ignore_index=True)
edges = edges.astype(int)
edges.drop_duplicates(keep='first', inplace=True)
edges.reset_index(inplace=True)
edges.drop(columns=['index'], inplace=True)
edges['capacity'] = edges['size']**2
#%%
"""
Flow through a pipeline is proportional to its transversal area. Therefore,
the capacity of an edge is computed as its size squared.
"""

#%% Build list of segments
lines = []
capacities = []
for index, row in edges.iterrows():
    id1 = row['id1']
    lon1 = vertices.loc[id1,:]['lon']
    lat1 = vertices.loc[id1,:]['lat']
    cord1 = (lon1, lat1)
    id2 = row['id2']
    lon2 = vertices.loc[id2,:]['lon']
    lat2 = vertices.loc[id2,:]['lat']
    cord2 = (lon2, lat2)
    lines.append([cord1, cord2])
    capacities.append(row['capacity'])
#%%
    
#%% Translate sizes into colors
colors_dict = {4:'#e41a1c', 9:'#377eb8', 16:'#4daf4a'}
colors = []
for cap in capacities:
    colors.append(colors_dict[cap])
#%%

#%% Plot the graph
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.lines import Line2D

plt.rcParams.update({'font.size': 30})
fig, ax = plt.subplots(figsize=(15,15))
ax.set_ylim(vertices.lat.min()-.002, vertices.lat.max()+.002)
ax.set_xlim(vertices.lon.min()-.01, vertices.lon.max()+.01)
plt.xlabel('Longitude')
plt.ylabel('Latitude')
line_segments = LineCollection(lines, colors=colors, linewidths=4)
ax.add_collection(line_segments)
custom_lines = [Line2D([0], [0], color=colors_dict.get(4), lw=3),
                Line2D([0], [0], color=colors_dict.get(9), lw=4),
                Line2D([0], [0], color=colors_dict.get(16), lw=4)]
ax.legend(custom_lines, [4, 9, 16], title='Capacity:')
plt.scatter(x=vertices['lon'], y=vertices['lat'], s=50, color='black')
plt.grid()
plt.savefig('graph.png')
#%%

#%% Export important data to files
vertices.to_csv('vertices.csv', sep=';')
edges.to_csv('edges.csv', sep=';')
#%%