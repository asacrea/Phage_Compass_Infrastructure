import dendropy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.gridspec import GridSpec
from minisom import MiniSom 

def difference (list1, list2):
    list_dif = [i for i in list1 + list2 if i not in list1 or i not in list2]
    return list_dif

t#ree = dendropy.Tree.get_from_path("/Users/andressacre/Documents/Universidad/Investigación_Thomas/Data/prove.nwk","newick")
#tree = dendropy.Tree.get_from_path("/Users/andressacre/Documents/Universidad/Investigación_Thomas/Data/nucleotide_all_vs_all_tree.nwk","newick")
#tree = dendropy.Tree.get_from_path("/hpcfs/home/c.sancheza/Bacteriophages/nucleotide_all_vs_all_tree_2.nwk", "newick")
phago_bacteria = pd.read_csv("/Users/andressacre/Documents/Universidad/Investigación_Thomas/Data/26Aug2019_phages_host_lineages.tsv", sep='\t')
#phago_bacteria = pd.read_csv("/Users/andressacre/Documents/Universidad/Investigación_Thomas/Data/26Aug2019_phages_hosts2.tsv", sep='\t')
#phago_bacteria = pd.read_csv("/hpcfs/home/c.sancheza/Bacteriophages/26Aug2019_phages_hosts.tsv", sep='\t')

n = list(enumerate(tree.taxon_namespace[:]))[len(list(enumerate(tree.taxon_namespace[:])))-1][0]

pdc = tree.phylogenetic_distance_matrix()

matrix = np.zeros((n+1,n+1))

for i, t1 in enumerate(tree.taxon_namespace[:-1]):
	for j, t2 in enumerate(tree.taxon_namespace[i+1:]):
		if((i+j+1)<=n):
			#if list_to_dict[t1.label] == list_to_dict [t2.label]:
				matrix[i][i+j+1] = pdc(t1,t2)

np.save("/Users/andressacre/Documents/Universidad/Investigación_Thomas/matrix", matrix)
np.save("/hpcfs/home/c.sancheza/Bacteriophages/matrix", matrix)

#Cargar matrix de distancias
input_f = "/Users/andressacre/Documents/Universidad/Investigación_Thomas/Data/nucleotide_dereplicated.tsv"
df = pd.read_csv(input_f, sep='\t')


#Leer solo primera linea del archivo
#f1 = open(input_f)
#names = [str(x) for x in f1.readline().split()]

#Filtrar matrix
compare = [phago_bacteria.loc[phago_bacteria['Phage accession'] == x, 'Host lineage'] for x in names]
real_names = [list(x.keys()) for x in compare if len(x.keys()) == 1]
#compare = phago_bacteria.loc[phago_bacteria['Phage accession'].isin(names)]

#compare2 = list(compare['Phage accession']) 
#noestan = difference(names, compare2)

#Organizar los indices
df.index = df['Unnamed: 0']
df = df.drop(['Unnamed: 0'], axis=1)

for x in noestan:
    df = df.drop([x], axis=0)
    df = df.drop([x], axis=1)

phago_bacteria.index = estan

compare = [phage_bacteria.loc[phage_bacteria['Phage accession', x] for x in enumerate(compare2) if phage_bacteria.loc[phage_bacteria['Phage accession', x] != compare2]]

#Delete rows aren't in phage_bacteria
for x in ennumarate(phago_bacteria['Phage accession']):
    if phago_bacteria.loc[phago_bacteria['Phage accession'] == x, 'Phage accession'].empty:
        phago_bacteria = phago_bacteria.drop([x], axis=0)

df_empty = pd.DataFrame(columns=['User_ID', 'UserName'))
for i in real_names
    
[phago_bacteria[x] for x in real_names]    
    
    

