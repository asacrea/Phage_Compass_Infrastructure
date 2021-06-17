#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 16:34:58 2020

@author: andressacre
"""

from tulip import tlp
from tulipgui import tlpgui
from loadData import LoadData

n = 100
load = LoadData(n)

#input_t = "/Users/andressacre/Data_Matrix/Taxonomies.tsv"

tax, n_tax = load.makeP()

graph = tlp.loadGraph("/Users/andressacre/results/out_7593.dot")

params = tlp.getDefaultPluginParameters("Simple", graph)
params["use node weights"] = True
# set custom spacing
params["ideal edge length"] = 100.0
params["minDistCC"] = 50.0

params_2 = tlp.getDefaultPluginParameters("To labels", graph)
params_2["edges"] = False

# get a reference to the default layout property
viewLayout = graph.getLayoutProperty("viewLayout")

#tlp.getAlgorithmPluginsList()
tlp.getLayoutAlgorithmPluginsList()

# call the layout algorithm and store the result in viewLayout
graph.applyLayoutAlgorithm("Frutcherman Reingold (OGDF)", viewLayout, params)
#graph.applyLayoutAlgorithm("FM^3 (OGDF)", viewLayout, params)

viewColor = graph.getColorProperty("viewColor")
externLabel = graph.getStringProperty("externLabel")

colors = [(255, 0, 0), (0, 255, 0), (0,0,255), (255,255,0), (229,208,18), (0,255,255), (201,201,201), (0,0,0)]

i = 0
for n in graph.getNodes():
    viewColor[n] = colors[p[int(externLabel[n])]]
    #viewColor[n] = tlp.Color(0, 255, 0)
    
#view = tlpgui.createNodeLinkDiagramView(graph)    
    
nodeLinkView = tlpgui.createView("Node Link Diagram view", graph, tlp.DataSet(), False)

renderingParams = nodeLinkView.getRenderingParameters()
# Save a snapshot of the view to an image file on disk
nodeLinkView.saveSnapshot("/Users/andressacre/Results/tulip_view_7593_FR.png", 1920, 1080)
    
    
    
    
    
    
    
    
    