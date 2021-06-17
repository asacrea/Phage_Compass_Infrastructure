#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 16:34:58 2020

@author: andressacre
"""
from os import path
from tulip import *
#from tulipogl import *
from tulipgui import *
from loadData import LoadData

class GraphTulip:
    n = 1000
    matrix_2 = None
    tax = None
    
    def __init__(self, n, upper_threshold = 0, bottom_threshold = 0):
        self.n = n
        load = LoadData(n)
        #Load Taxonomies
        tax, n_tax = load.makeP()
        
        params = tlp.getDefaultPluginParameters('Adjacency Matrix')
        
        if bottom_threshold == 0:
            print(upper_threshold)
            params['filename'] = "/Users/andressacre/Data_Matrix/prueba_threshold_" \
                    +str(upper_threshold)[-1]+ "_" + str(self.n) +".tsv"
        else:
            params['filename'] = "/Users/andressacre/Data_Matrix/prueba_threshold_" \
                    + str(upper_threshold)[-1] + "_" + str(bottom_threshold)[-1]+ "_" + str(self.n) + ".tsv"
        graph = tlp.importGraph('Adjacency Matrix', params)

        # get a reference to the default layout property
        # Get references to some view properties
        viewLayout = graph.getLayoutProperty("viewLayout")
        viewSize = graph.getSizeProperty("viewSize")
        viewBorderWidth = graph.getDoubleProperty("viewBorderWidth")
        viewLabelBorderWidth = graph.getDoubleProperty("viewLabelBorderWidth")
        viewColor = graph.getColorProperty("viewColor")
        viewLabelColor = graph.getColorProperty("viewLabelColor")
        viewLabelBorderColor = graph.getColorProperty("viewLabelBorderColor")
        viewBorderColor = graph.getColorProperty("viewBorderColor")
        viewColor = graph.getColorProperty("viewColor")
        viewLabel = graph.getStringProperty("viewLabel")
        viewShape = graph.getIntegerProperty("viewShape")
        externLabel = graph.getStringProperty("externLabel")
        weights = graph.getDoubleProperty("weights")

        # Compute an anonymous degree property
        degree = tlp.DoubleProperty(graph)
        degreeParams = tlp.getDefaultPluginParameters("Degree")
        graph.applyDoubleAlgorithm("Degree", degree, degreeParams)
        #
        params_2 = tlp.getDefaultPluginParameters("To labels", graph)
        params_2["edges"] = False
        
        # Apply an FM^3 layout on it
        params = tlp.getDefaultPluginParameters("Frutcherman Reingold (OGDF)", graph)
        params["use node weights"] = True
        # set custom spacing
        params["ideal edge length"] = 1000.0
        params["Unit edge length"] = 50.0
        #params["minDistCC"] = 1500.0
        
        #Algorithms to apply over the graph
        #graph.applyLayoutAlgorithm("Frutcherman Reingold (OGDF)", viewLayout, params)
        graph.applyLayoutAlgorithm("FM^3 (OGDF)", viewLayout, params)

        # My colors
        colors = [(255, 0, 0), (0, 255, 0), (0,0,255), (255,255,0), \
                  (229,208,18), (0,255,255), (201,201,201), (0,0,0)]
        
        for i,n in enumerate(graph.getNodes()):
            #viewColor[n] = colors[tax[int(externLabel[n])]]
            viewColor[n] = colors[tax[i]]
            #viewColor[n] = tlp.Color(0, 255, 0)
        '''
        for e in graph.getEdges():
            print(graph['viewMetric'][e])
            #print(str(graph.source(e)) + " a " + str(graph.target(e)) + " weight: " +str(weights(e)))
        '''
        view = tlpgui.createNodeLinkDiagramView(graph)    
        
        # Set border colors values
        viewLabel.setAllNodeValue("")
        viewBorderColor.setAllEdgeValue(tlp.Color(0, 255, 0, 0)) 
        viewColor.setAllEdgeValue(tlp.Color(0, 255, 0, 0)) 
        viewBorderColor.setAllNodeValue(tlp.Color.Green)
        viewLabelColor.setAllNodeValue(tlp.Color.Red)
        viewLabelBorderColor.setAllNodeValue(tlp.Color.Red)
        
        # Add a border to nodes/edges
        viewBorderWidth.setAllNodeValue(0)
        viewBorderWidth.setAllEdgeValue(0)
        
        # Sets nodes shapes to circle
        viewShape.setAllNodeValue(tlp.NodeShape.Circle)

        # Create a Node Link Diagram view and set some rendering parameters
        nodeLinkView = tlpgui.createNodeLinkDiagramView(graph)
        renderingParameters = nodeLinkView.getRenderingParameters()
        renderingParameters.setViewArrow(False)
        renderingParameters.setMinSizeOfLabel(0)
        nodeLinkView.setRenderingParameters(renderingParameters)
        
        #nodeLinkView = tlpgui.createView("Node Link Diagram view", graph, \
        #                                 tlp.DataSet(), False)
        #renderingParams = nodeLinkView.getRenderingParameters()
        # Save a snapshot of the view to an image file on disk
        nodeLinkView.saveSnapshot("/Users/andressacre/Results/Image/Tulip/tulip_view_Threshold" \
                                  +str(n)+"_"+str(upper_threshold)[-1]+"_FR.png", 1920, 1080)
            
if __name__ == '__main__':
    l = GraphTulip()
        
        
        
        
        
        
        