# -*- coding: utf-8 -*-
#!/usr/bin/python
import json
import copy
from loadData import *
import numpy as np
import pygraphviz
import networkx as nx
import matplotlib.pyplot as plt
from graphviz import Digraph
from pyvis.network import Network
from networkx.drawing.nx_agraph import to_agraph
from networkx.drawing.nx_agraph import pygraphviz_layout
from networkx.drawing.nx_agraph import write_dot
from concurrent.futures import ThreadPoolExecutor

class MakeGraphvizGraph:
    n = 0
    G = None
    G_2 = None
    matrix_2 = None
    p_2 = None
    upper_threshold = 0
    bottom_threshold = 0
    
    def __init__(self,n, upper_threshold = 0, bottom_threshold = 0):
        ##Assign global variables
        self.n = n
        self.upper_threshold = upper_threshold
        self.bottom_threshold = bottom_threshold
        #self.matrix_2 = matrix
        load = LoadData(self.n)
        if bottom_threshold == 0:
            self.matrix_2 = load.makeMatrix(upper_threshold, False)
        else:
            self.matrix_2 = load.makeMatrix(upper_threshold, bottom_threshold, False)
        #Load matix & taxonomies

        self.tax, self.n_tax = load.makeP()
        #Create networkx graph
        self.makeGraphs()
        #self.graphPyVis()
        #self.graphGraviz()
        #self.writeDOT()
    
    def makeGraphs(self):
        dt = [('len', float)]
        #A = self.matrix_2
        A = matrix_2.view(dt)
        print("Reading Numpy matrix")
        self.G = nx.from_numpy_matrix(A)
        print("Naming edges") 
        self.G = nx.relabel_nodes(self.G, dict(zip(range(len(self.G.nodes())), \
                                                   self.n_tax)))
        G_2 = copy.copy(self.G)
        
        print("Deleting innecesary edges")
        to_remove = []
        for i, edge in enumerate(self.G_2.edges.data()):
            a = edge[0]
            b = edge[1]
            #print(edge[2]['len'])
            if(edge[2]['len'] == 0):
                to_remove.append((a,b))
        #Remove all nodes which weight be 1        
        [self.G.remove_edge(*r) for r in to_remove]
        ceros = [x for x, y in G.degree if G.degree[x] == 0]
        G.remove_nodes_from(ceros)
        #nx.write_gpickle(G, "test.gpickle")
        '''for node in self.G:
            print(node)
            color_map.append(colors[self.tax[int(node)]])
        '''    
    
    def getMetrics():
        #Degree of each node
        degree = list(G.degree)
        distri = [G.degree[x] for x, y in G.degree]
        ceros = [x for x, y in G.degree if G.degree[x] == 0]
        #Density coeficient
        density = nx.density(G)
        #Grouping coeficient
        clustering = nx.triangles(G)
        
        #Minimon and maximun degree value
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
    
    def graphGraviz(self, algorithm = 'sfdp'):
        #Networkx to Graphviz
        G = to_agraph(self.G)
        print(type(G))        
        #Define colors
        colors = ["lawngreen", "indigo", "orange", "red", "yellow", "cyan", \
                  "gray", "lightseagreen"]
        try:
            for i, node in enumerate(G.iternodes()):
                #G.node(str(i), **{'width':str(5), 'height':str(5)})
                #g.node(str(i), **{'width':str(i), 'height':str(i)})
                node.attr.update(color = colors[self.tax[int(node)]], style = "filled", height = 0.02, width = 0.02, fixedsize = True, labelfontsize = 100, label = "")
            #print(node.attr['color'])
        except:
            print("Error del paquete, pero pinta")
        print("Creo que pinté")
        
        G.edge_attr.update(color="#40e0d000", width="1.0")
        
        G.draw('/Users/andressacre/Results/Image/Graphviz/out_SFDP_'+  '_' + str(self.upper_threshold)[-1] + '_' + str(self.bottom_threshold)[-1] + "_" +str(self.n)+'.png', \
               format='png', prog=algorithm)
        try:
            for i, node in enumerate(G.iternodes()):
                #G.node(str(i), **{'width':str(5), 'height':str(5)})
                #g.node(str(i), **{'width':str(i), 'height':str(i)})
                node.attr.update(shape = "box")

            #print(node.attr['color'])
        except:
            print("Error del paquete, pero pinta")
        print("Creo que pinté")

        G.draw('/Users/andressacre/Results/Image/Graphviz/out_SFDP_'+  '_' + str(self.upper_threshold)[-1] + '_' + str(self.bottom_threshold)[-1] + "_" +str(self.n)+'_2.png', format='png')
 
    def graphPyVis(self):
        executor = ThreadPoolExecutor()
        #Define colors
        colors = ["lawngreen", "indigo", "orange", "red", "yellow", "cyan", \
                  "gray", "lightseagreen"]
        shapes = ["dot", "diamond", "ellipse", "star", "triangle", "triangleDown", \
                  "square", "box"]
        nt = Network("800px", "800px")
        # populates the nodes and edges data structures
        #nt.from_nx(self.G)
        #nodes = self.G.nodes.data()
        #edges = self.G.edges.data()
        print("Making Pyvis graph")
        for node in self.G.nodes.data():
            nt.add_node(node[0], color = colors[self.tax[int(node[0])]], shape = shapes[self.tax[int(node[0])]],size = 10)            
        print("Making relationship")
        
        start_time = time()
        for edge in self.G.edges.data():
            executor.submit(nt.add_edge, edge[0], edge[1], hidden = True, weight=edge[2]['len'])
            #nt.add_edge(edge[0], edge[1], hidden = True, weight=edge[2]['len'])
        elapsed_time = time() - start_time
        print("Parallel time: "+str(elapsed_time))

        #nt_2 = copy.copy(nt)
        print("Working getting final positions of nodes")        
        nt.force_atlas_2based(gravity=-31, central_gravity=0.025, spring_length=200, spring_strength=0.08, damping=0.4, overlap=0)
        #nt.hrepulsion(node_distance=120, central_gravity=0.0, spring_length=100, spring_strength=0.01, damping=0.09)
        #print("Graphing")
        nt.show("nx.html")
        return nt
        
        
    def writePositions(self):
        pos = pygraphviz_layout(self.G_2, prog = 'dot')
        with open('/hpcfs/home/c.sancheza/Bacteriophages/Results/Graphs/Graphviz/file.txt', 'w') as file:
             file.write(json.dumps(pos))
             
    def writeDOT(self):
        try:
            #Create .DOT file
            write_dot(self.G_2, '/Users/andressacre/Results/Dot_File/out_'+ \
                      str(self.upper_threshold)[-1] + '_' + str(self.bottom_threshold)[-1] + str(self.n)+'.dot')
        except:
            print("Escribí con algunos errores en compilación")

if __name__ == '__main__':
    l = MakeGraphvizGraph()


