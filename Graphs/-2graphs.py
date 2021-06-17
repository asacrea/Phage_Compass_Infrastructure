# -*- coding: utf-8 -*-
#!/usr/bin/python
import sys
import json
import string
import random
import numpy as np
import pandas as pd
import networkx as nx
import pygraphviz
from graphviz import Digraph
from networkx.drawing.nx_agraph import to_agraph
from networkx.drawing.nx_agraph import pygraphviz_layout
from networkx.drawing.nx_agraph import write_dot

input_m = "/Users/andressacre/Data_Matrix/Data.tsv"
input_t = "/Users/andressacre/Data_Matrix/Taxonomies.tsv"

matrix = pd.read_csv(input_m, sep='\t', header = None)
matrix = matrix.to_numpy()

l = np.array(list(random.sample(range(0,7593),7593)))

matrix_2 = matrix[l[:,None],l]
matrix_2[matrix_2 == 1] = 0


phago_bacteria = pd.read_csv(input_t, sep='\t')

phage_range = range(0,len(phago_bacteria.index))
phylum = [json.loads(phago_bacteria['Host lineage'][i].replace("'","\""))['phylum'] for i in phage_range]
phylum = [x[0] for x in phylum]
phago_bacteria["Guest"] = phylum
target = phago_bacteria["Guest"].value_counts()
target = target[target >= 20].index

relevant = {x:i for i, x in enumerate(target)}

phago_bacteria["Value"] = len(relevant)
for p in target:
	phago_bacteria.loc[phago_bacteria['Guest'] == p, 'Value'] = relevant[p]

target = list(target)
target.append("Others")

p = phago_bacteria["Value"][l]

type_counts = phago_bacteria['Guest'].value_counts()
type_counts = phago_bacteria['Value'].value_counts()
df2 = pd.DataFrame(type_counts)
print(df2)

type_counts.plot.pie(y='Guest')


p_2 = list(p.index)

#colors = [str(i) for i in range(0,len(relevant)+1)]
colors = ["lime", "indigo", "orange", "red", "yellow", "cyan", "gray", "lightseagreen"]

dt = [('len', float)]

A = matrix_2
A = A.view(dt)

G = nx.from_numpy_matrix(A)
G = nx.relabel_nodes(G, dict(zip(range(len(G.nodes())),p_2)))    

G_2 = nx.from_numpy_matrix(A)
G_2 = nx.relabel_nodes(G_2, dict(zip(range(len(G_2.nodes())),p_2)))    
nx.write_dot(G_2, '/tmp/out.dot')
pos = pygraphviz_layout(G_2, prog = 'dot')
print(pos)

G = to_agraph(G)

for i, node in enumerate(G.iternodes()):
    #print(node.attr['color'])
    node.attr.update(color = colors[p[int(node)]], style = "filled")

#G.node_attr.update(color="indigo", style="filled")
G.edge_attr.update(color="#40e0d000", width="1.0")

G.draw('out_3.png', format='png', prog='fdp')









