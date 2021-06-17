import dendropy
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from minisom import MiniSom 

#tree = dendropy.Tree.get_from_path("/Users/andressacre/Documents/Universidad/Investigación_Thomas/Data/nucleotide_all_vs_all_tree_2.nwk","newick")
tree = dendropy.Tree.get_from_path("/Users/andressacre/Documents/Universidad/Investigación_Thomas/Data/prove.nwk", "newick")
phago_bacteria = pd.read_csv("/Users/andressacre/Documents/Universidad/Investigación_Thomas/Data/26Aug2019_phages_hosts2.tsv", sep='\t')

#list_to_dict = {phago_bacteria[0][i]: phago_bacteria[1][i] for i in range(0, len(phago_bacteria[0]))}

#print(list_to_dict["MG945723.1"])

n = list(enumerate(tree.taxon_namespace[:-1]))[len(list(enumerate(tree.taxon_namespace[:-1])))-1][0]
print(n)
pdc = tree.phylogenetic_distance_matrix()
#np.save("/Users/andressacre/Documents/Universidad/Investigación_Thomas/matrix", pdc)
#np.load("/hpcfs/home/c.sancheza/Bacteriophages/matrix.npy")

matrix = np.zeros((n+1,n+1))
index = []
for i, t1 in enumerate(tree.taxon_namespace[:-1]):
	for j, t2 in enumerate(tree.taxon_namespace[i+1:]):
		if((i+j+1)<=32):
			#print("FIla '%s', Coumna ''%s" % (i,i+j+1))
			#if list_to_dict[t1.label] == list_to_dict [t2.label]:
				matrix[i][i+j+1] = pdc(t1,t2)
			#print(matrix[i][j])
			#print("Distance between '%s' and '%s': %s" % (t1.label, t2.label, pdc(t1, t2)))
	#print(i)
	index.append(t1.label)


#table2 = pd.DataFrame(matrix, index=index, columns=index)
#print(table2)

#matrix = np.array([6, 7, 8]).reshape(3,1)
#print(matrix.shape)
#matrix = np.arange(2).reshape(2,1)
#print(matrix.shape)

som = MiniSom(6, 6, n+1, sigma=0.5, learning_rate=0.5)
som.train_random(matrix, 100)


#Plotting the response for each pattern in the iris dataset
plt.pcolor(som.distance_map().T, cmap='jet')  # plotting the distance map as background


target = phago_bacteria['Guest'].value_counts()
target = target[target >= 1].index
relevant = {x:i for i, x in enumerate(target)}

phago_bacteria["Value"] = len(relevant)

for p in target:
	phago_bacteria.loc[phago_bacteria['Guest'] == p] = relevant[p]

#print(phago_bacteria["Value"])
t = phago_bacteria["Value"]

colors = ["C"+str(i) for i in range(0,len(relevant))]
print(colors)
for cnt, xx in enumerate(matrix):
    w = som.winner(xx)  # getting the winner
    print(t[cnt])
    print(colors[t[cnt]])
    # palce a marker on the winning position for the sample xx
    plt.plot(w[0]+.5, w[1]+.5, markerfacecolor='None',
            markeredgecolor=colors[t[cnt]], markersize=34, markeredgewidth=2)
plt.axis([0, 6, 0, 6])
plt.savefig('/Users/andressacre/Documents/Universidad/Investigación_Thomas/SOM_prove.png')
plt.show()






