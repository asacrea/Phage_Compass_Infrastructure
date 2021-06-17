#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 10:04:25 2021

@author: andressacre
"""

nt_2 = Network("800px", "800px")

print("Making Pyvis graph")
print("Creating nodes")
for node in G.nodes.data():
    tar = str(node[0]) + "<br>" + target[tax[int(node[0])]] 
    nt_2.add_node(node[0], color = colors[tax[int(node[0])]], \
                shape = shapes[tax[int(node[0])]],size = 10, \
                title = tar)

print("Making relationship")
#start_time = time()
for edge in G.edges.data():
    if (edge[0] == 1870 or edge[1] == 1870):
        print("("+str(edge[0])+", "+str(edge[1])+") : " + str(edge[2]))
    executor.submit(nt_2.add_edge, edge[0], edge[1], value=edge[2]['len'])

nt_2.show_buttons(filter_=['physics'])
nt_2.force_atlas_2based(gravity=-31, central_gravity=0.025, spring_length=200, spring_strength=0.08, damping=0.4, overlap=0)
#nt.hrepulsion(node_distance=120, central_gravity=0.0, spring_length=100, spring_strength=0.01, damping=0.09)
nt_2.show("../../Results/PyVis/nx_prueba_2_con.html")
