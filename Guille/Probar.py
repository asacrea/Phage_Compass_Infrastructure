#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 13:15:24 2021

@author: andressacre
"""

mash_dist_file = snakemake.input.mashtbl
print('Creating phage intergenomic distance network...')
mash_dist_df = pd.read_csv(mash_dist_file, sep = '\t')
mash_dist_df = mash_dist_df.set_index('#query')
graph_file = snakemake.output.plaingraph
G = nx.from_numpy_matrix(mash_dist_df.values)
labels = mash_dist_df.columns.values
G = nx.relabel_nodes(G, dict(zip(range(len(labels)), labels)))
keep_edges = [(x,y) for x,y,z in G.edges(data = True) if pd.notnull(z['weight'])]
Gmod = nx.Graph(G.edge_subgraph(keep_edges))
singletons = []
for item in mash_dist_df.itertuples(index = True):
	non_null_values = [x for x in item[1:] if pd.notnull(x)]
	if len(non_null_values) == 1:
		singletons.append(item[0])
Gmod.add_nodes_from(singletons)