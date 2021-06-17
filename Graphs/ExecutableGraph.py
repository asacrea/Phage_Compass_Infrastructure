# -*- coding: utf-8 -*-
#!/usr/bin/python

import copy
import numpy as np
import random
import networkx as nx
from loadData import *
import matplotlib.pyplot as plt
#from graphviz import  Digraph
from pyvis.network import Network
from networkx.drawing.nx_agraph import to_agraph
from networkx.drawing.nx_agraph import pygraphviz_layout
from networkx.drawing.nx_agraph import write_dot
from concurrent.futures import ThreadPoolExecutor

#n = 7593
n = 2000
upper_threshold = 0.4
bottom_threshold = 0.0

load = LoadData(n)

matrix_2 = load.makeMatrix(upper_threshold, bottom_threshold, False)
tax, n_tax, target = load.makeP()

tax_g, n_tax_g, target_g = load.makeGen()

dt = [('len', float)]
#A = self.matrix_2
matrix_2 = matrix_2.view(dt)

G = nx.from_numpy_matrix(matrix_2)

#G = nx.relabel_nodes(G, dict(zip(range(len(G.nodes())), n_tax)))
G = nx.relabel_nodes(G, dict(zip(range(len(G.nodes())), n_tax_g)))
G_2 = copy.copy(G)


to_remove = []
for a, b, p in G_2.edges.data():
    print(p['len'])
    if(p['len'] == 0):
        to_remove.append((a,b))
        
#Remove all nodes which weight be 0        
[G.remove_edge(*r) for r in to_remove]
ceros = [x for x, y in G.degree if G.degree[x] <= 10]
G.remove_nodes_from(ceros)
degree = list(G.degree)
degree_dict = dict(degree)

r = nx.degree_assortativity_coefficient(G)
sub_c = nx.subgraph_centrality(G)

#centroid = [x for x, y in G.degree if G.degree[x] >= 150 and G.degree[x] <= 180]
#len([x for x in tax[centroid].index if tax[x] == 2])
'''
for c in range(0,8):
    #get nodes with specific color
    color_index = tax[tax == c].index
    color_degree = [(k, degree_dict[k]) for k in color_index if k in degree_dict]

    #Verify which important nodes don't have connections between with nodes 
    #of the same color
    c_edges = [(a,b) for a,b,w in G.edges.data() if a in color_index or b in color_index]
    for x,y in color_degree:
        for z in range(round(len(color_degree)*0.05)):
            rand_value = color_degree[random.randrange(0, len(color_degree))][0]
            couple = (x,rand_value)
            if couple not in G.edges:
                G.add_edge(x, rand_value, len=0.5)
'''              

for a, b, p in G.edges.data():
    if (a == 1933):
        print("("+str(a)+", "+str(b)+")")
    #if(tax[a] == 2 and tax[b] == 2 and p['len'] < 0.76):
     #   print(p['len'])
        #p['len'] = p['len'] * 1.9


#Parallel object
executor = ThreadPoolExecutor()

#Define parameters
colors = ["lawngreen", "indigo", "orange", "red", "yellow", "cyan", \
          "gray", "lightseagreen"]
'''
colors = ["#231C07", "#392A16", "#634133", "#B86F52", "#F78764", "#CB9173", \
          "#E0D68A", "#6E9075","#78C091", "#81F0E5", "#B4436C", "#E27396", \
          "#EA9AB2", "#EFCFE3", "#86CB92", "#404E7C", "#251F47", "#AB4E68",\
          "#9D9171", "#C4A287", "#F5A6E6", "#05A8AA", "#B8D5B8", "#1E555C", \
          "#61988E", "#DAFF7D","#B2EF9B","#EB5160", "#E5E5E5", "#FFFFFF", "#BFBCCB"]
shapes = ["dot", "diamond", "ellipse", "star", "triangle", "triangleDown", \
          "square", "box", "dot", "diamond", "ellipse", "star", "triangle", "triangleDown", \
          "square", "box", "dot", "diamond", "ellipse", "star", "triangle", "triangleDown", \
          "square", "box", "dot", "diamond", "ellipse", "star", "triangle", "triangleDown", \
          "square"]
'''
#node_titlesd = {x: f'{}<br>Target host genera:<br>{colors[tax[int(node[0])]}<br>Phage genus:<br>{y["phage_genus"]}' for x,y in G.nodes(data = True)}
#edge_titlesd = {(x,y):z['weight'] for x,y,z in hostgraph.edges(data = True)}
#nx.set_node_attributes(hostgraph, node_titlesd, 'title')


#Create Pyvis Graph
nt = Network("800px", "800px")

print("Making Pyvis graph")
print("Creating nodes")
'''
for node in G.nodes.data():
    tar = str(node[0]) + "<br>" + target_g[tax_g[int(node[0])]] 
    nt.add_node(node[0], color = colors[tax_g[int(node[0])]], \
                shape = shapes[tax_g[int(node[0])]],size = 10, \
                title = tar)
'''
for node in G.nodes.data():
    tar = str(node[0]) + "<br>" + target[tax[int(node[0])]] 
    nt.add_node(node[0], color = colors[tax[int(node[0])]], \
                size = 10, \
                title = tar)
#distri = [G.degree[x] for x, y in G.degree]

print("Making relationship")
#start_time = time()
for edge in G.edges.data():
    #if (edge[0] == 1757):
    #    print("("+str(edge[0])+", "+str(edge[1])+") : " + str(edge[2]))
    #executor.submit(nt.add_edge, edge[0], edge[1], value=edge[2]['len'])
    nt.add_edge(edge[0], edge[1], hidden=True,weight=edge[2]['len'])
#elapsed_time = time() - start_time
#print("Parallel time: "+str(elapsed_time))

#nt_2 = copy.copy(nt)

nt.show_buttons(filter_=['physics'])
nt.force_atlas_2based(gravity=-31, central_gravity=0.025, spring_length=200, spring_strength=0.08, damping=0.4, overlap=0)
#nt.hrepulsion(node_distance=120, central_gravity=0.0, spring_length=100, spring_strength=0.01, damping=0.09)
print("Finish getting positions")
nt.show("../../Results/PyVis/pviz_phyla.html")



'''
distri = [G.degree[x] for x, y in G.degree]
min = np.amin(distri)
max = np.amax(distri)

#Get distribution degree
df_nu = pd.Series(distri)
counts = df_nu.value_counts(bins=50)
max_rep = list(counts)[0]

plt.xlim((min,max+100))
plt.ylim((0, max_rep+100))
plt.hist(distri, bins = 50)
plt.show()
distri[distri == 0]
[(a,b,w) for a,b,w in G.edges.data() if a == 1202]
[(a['from'],a['to'],a['value']) for a in nt.edges if a["from"]== 134]
'''