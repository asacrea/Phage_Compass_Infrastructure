#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 09:45:56 2020

@author: andressacre
"""

from graphs import *
from loadData import *
#from graph_tulip import *
from time import time

#############################Graphviz & Networkx############################
#Initializing time

#Sub sammple number of nodes
n = 7593
#Make a graph
#load = LoadData(n)
#matrix = load.makeMatrix(False)

graphs = MakeGraphvizGraph(n, 0.8, 0.1)
start_time = time()
nt = graphs.graphPyVis()
#Measure time
elapsed_time = time() - start_time
print(elapsed_time)

for node in nt.nodes:
    if node['color'] == 'indigo':
        node['color'] = 'purple'
        #print(node['color'])
nt.show("nx.html")

'''
############################# Tulip ############################
#Initializing time
start_time = time()
#Sub sammple number of nodes
n = 7593
load = LoadData(n)
matrix_2 = load.makeMatrix(0.5, 0.0, True)
#Make a graph
graphs_2 = GraphTulip(n, 0.5, 0.0)
elapsed_time = time() - start_time
print(elapsed_time)

start_time = time()
matrix_2 = load.makeMatrix(0.4, 0.0, True)
#Make a graph
graphs_2 = GraphTulip(n, 0.4, 0.0)
elapsed_time = time() - start_time
print(elapsed_time)

start_time = time()
matrix_2 = load.makeMatrix(0.3, 0.0, True)
#Make a graph
graphs_2 = GraphTulip(n, 0.3, 0.0)
elapsed_time = time() - start_time
print(elapsed_time)

start_time = time()
matrix_2 = load.makeMatrix(0.2, 0.0, True)
#Make a graph
graphs_2 = GraphTulip(n, 0.2, 0.0)
elapsed_time = time() - start_time
print(elapsed_time)

start_time = time()
matrix_2 = load.makeMatrix(0.8, 0.4, True)
#Make a graph
graphs_2 = GraphTulip(n, 0.8, 0.4)
#Measure time
elapsed_time = time() - start_time
print(elapsed_time)
'''