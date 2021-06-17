import pandas as pd
import numpy as np
from minisom import MiniSom
import matplotlib.pyplot as plt
from skbio.tree import TreeNode

from cycler import cycler
mpl.rcParams['axes.prop_cycle'] = cycler(color='bgrcmyk')

newick_tree = open("/Users/andressacre/Documents/Universidad/Investigación_Thomas/nucleotide_all_vs_all_tree.nwk", "r").readlines()

tree = TreeNode.read(newick_tree)
tree = tree.root_at_midpoint()

table = pd.read_csv("/Users/andressacre/Documents/Universidad/Investigación_Thomas/26Aug2019_phages_hosts.tsv", sep='\t', header=None)
#table = open("/Users/andressacre/Documents/Universidad/Investigación_Thomas/nucleotide_all_vs_all_tree.nwk", "r").readlines()

sample_ids = [table[0]]
features_ids = [table[0]]
data = np.zeros((len(table[0]),len(table[0])))

d_table = pd.DataFrame(data, index=sample_ids, columns=features_ids)

def get_phylogenetic_distances(tree, table, verbose=False):
    observed_otus = [obs_id for obs_id in table[0]]
    observed_nodes = set()
    phylogenetic_distance = []

    # iterate over the observed OTUs
    for i, otu in enumerate(observed_otus):
        t = tree.find(otu)
        observed_nodes.add(t)
        if verbose:
            print(t.name, t.length, end=' ')
        for internal_node in t.ancestors():
            if internal_node.length is None:
                # we've hit the root
                if verbose:
                    print('')
            else:
                if verbose:
                    print(internal_node.length, end=' ')
                observed_nodes.add(internal_node)
        phylogenetic_distance.append(sum(o.length for o in observed_nodes))
    return phylogenetic_distance

phylogenetic_distance = get_phylogenetic_distances(tree, table, verbose=False)
phylogenetic_distance = np.asarray(phylogenetic_distance).reshape(len(phylogenetic_distance),1)

som = MiniSom(30, 30, 1, sigma=0.5, learning_rate=0.5)
som.train_random(phylogenetic_distance, 100)

plt.figure(figsize=(7, 7))
# Plotting the response for each pattern in the iris dataset
plt.pcolor(som.distance_map().T, cmap='bone_r')  # plotting the distance map as background

target = np.genfromtxt("/Users/andressacre/Documents/Universidad/Investigación_Thomas/26Aug2019_phages_hosts.tsv", delimiter='\t', usecols=(1), dtype=str)
t = np.zeros(len(target), dtype=int)

unique_values = np.unique(table[1])
for i in range(len(unique_values)):
	t[target == unique_values[i]] = i

markers = ['o', 's', 'D']
colors = ['C0', 'C1', 'C2']
for cnt, xx in enumerate(data):
    w = som.winner(xx)  # getting the winner
    # palce a marker on the winning position for the sample xx
    plt.plot(w[0]+.5, w[1]+.5, markers[t[cnt]], markerfacecolor='None',
             markeredgecolor=colors[t[cnt]], markersize=12, markeredgewidth=2)
plt.axis([0, 7, 0, 7])
plt.savefig('resulting_images/som_iris.png')
plt.show()



