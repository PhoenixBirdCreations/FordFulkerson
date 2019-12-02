# -*- coding: utf-8 -*-
"""
Data downloaded from: http://konect.uni-koblenz.de/networks/foodweb-baywet
"""

#%%
"""
Import the data and name the columns. Round the feed_factor to an integer
and delete edges with feed_factor = 0.
"""
import pandas as pd
fla = pd.read_csv("foodweb-baywet/out.foodweb-baywet", delimiter=r"\s+", 
                  index_col=False, comment="%", header=None)
fla.columns = ['from', 'to', 'capacity']
fla.capacity = fla.capacity.astype(int)
fla = fla[fla.capacity > 0]
#%%

#%%
"""
Choose random source and target and display directed weighthed graph.
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
from random import choice

myG = nx.from_pandas_edgelist(fla, source='from', target='to', 
                              edge_attr=['capacity'], 
                              create_using=nx.MultiDiGraph())
s = choice(list(myG.nodes))
t = choice(list(myG.nodes))

def plot_initial_graph(G, s, t):
    pos = nx.layout.circular_layout(G, scale=2)
    plt.figure(figsize=(12,12))
    node_sizes = 500
    node_colors=[]
    for node in G:
        if node==s:
            node_colors.append('blue')
        elif node==t:
            node_colors.append('red')
        else:
            node_colors.append('black')
    edge_colors = list(nx.get_edge_attributes(G, 'capacity').values())
    cmap = 'Spectral'
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, 
                                   node_color=node_colors)
    nx.draw_networkx_labels(G, pos, font_size=16, font_color='white', 
                            font_weight='bold')
    edges = nx.draw_networkx_edges(G, pos, node_size=node_sizes, 
                                   arrowstyle='->', arrowsize=20, 
                                   edge_color=edge_colors,
                                   edge_cmap=plt.get_cmap(cmap), width=3)
    if (edges):
        pc = mpl.collections.PatchCollection(edges, cmap=plt.get_cmap(cmap))
        pc.set_array(edge_colors)
        plt.colorbar(pc)
    ax = plt.gca()
    ax.set_axis_off()
    plt.show()
    
plot_initial_graph(myG, s, t)
#%%

#%%
# push 0 flow through the graph
nx.set_edge_attributes(myG, 0, 'flow')

"""
Function that computes the residual graph
"""
def residual_graph(G):
    # dicts of capacities and flow through the edges of the graph
    capacities = nx.get_edge_attributes(G, 'capacity')
    flows = nx.get_edge_attributes(G, 'flow')
    # residual graph
    resG = nx.MultiDiGraph()
    for node in list(G.nodes):
        resG.add_node(node)
    # residual capacities
    for edge in list(G.edges):
        cap = capacities[edge]
        fl = flows[edge]
        resG.add_edge(edge[0], edge[1], capacity=cap-fl)
        resG.add_edge(edge[1], edge[0], capacity=fl)
    # delete edges with capacity lower or equal to 0
    res_cap = nx.get_edge_attributes(resG, 'capacity')
    for edge in list(resG.edges):
        if (res_cap[edge] <= 0):
            resG.remove_edge(*edge[:2])  
    return resG

resG = residual_graph(myG)
plot_initial_graph(resG, s, t)
#%%

#%%
"""
Check that initially a graph with 0 flow and its residual are equal. dif 
corresponds to the graph with the same vertex set as myG and resG, but with 
the edges in myG that do not exist in resG. Let's check that it returns a 
graph with no edges.
"""
dif = nx.difference(myG, resG)
plot_initial_graph(dif, s, t)
#%%

#%%
"""
Breadth-first search: search for the shortest path between two nodes by
implementing breadth-first search. When introduced in the Ford-Fulkerson
algorithm, it is equivalent to Dinic's algorithm
"""

def augmenting_path(G, s, t):
    
    # return a tuple of (True, bottleneck, [list of nodes in path])
    # if there is not a path: return (False, 0, empty-list)
#%%
    
#%%
"""
Push flow along a path
"""
def push_flow(G, flow, path):
    
#%%
    
#%%
"""
Ford-Fulkerson
"""
progress = []
progress.append((0, myG))
aug_path = augmenting_path(resG, s, t)
while (aug_path[0]):
    bottleneck = aug_path[1]
    path = aug_path[2]
    newG = push_flow(myG, bottleneck, path)
    myG = newG
    progress.append((bottleneck, myG))
    resG = residual_graph(myG)
    aug_path = augmenting_path(resG, s, t)
#%%
    
# https://ndres.me/post/matplotlib-animated-gifs-easily/