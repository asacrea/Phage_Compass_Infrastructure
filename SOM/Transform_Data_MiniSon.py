import dendropy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from minisom import MiniSom 

#tree = dendropy.Tree.get_from_path("/Users/andressacre/Documents/Universidad/Investigación_Thomas/Data/nucleotide_all_vs_all_tree_2.nwk","newick")
tree = dendropy.Tree.get_from_path("/Users/andressacre/Documents/Universidad/Investigación_Thomas/Data/prove.nwk", "newick")
phago_bacteria = pd.read_csv("/Users/andressacre/Documents/Universidad/Investigación_Thomas/Data/26Aug2019_phages_hosts2.tsv", sep='\t')

n = list(enumerate(tree.taxon_namespace[:]))[len(list(enumerate(tree.taxon_namespace[:])))-1][0]
print(n)
pdc = tree.phylogenetic_distance_matrix()
#np.save("/Users/andressacre/Documents/Universidad/Investigación_Thomas/matrix", pdc)
#np.load("/hpcfs/home/c.sancheza/Bacteriophages/matrix.npy")

matrix = np.zeros((34,34))
index = []
for i, t1 in enumerate(tree.taxon_namespace[:-1]):
	for j, t2 in enumerate(tree.taxon_namespace[i+1:]):
		if((i+j+1)<=33):
			#if list_to_dict[t1.label] == list_to_dict [t2.label]:
				matrix[i][i+j+1] = pdc(t1,t2)
	index.append(t1.label)

som = MiniSom(6, 6, n+1, sigma=0.5, learning_rate=0.5)
som.train_random(matrix, 100)


#Plotting the response for each pattern in the iris dataset
#plt.pcolor(som.distance_map().T, cmap='jet')  # plotting the distance map as background
#plt.colorbar()

target = phago_bacteria['Guest'].value_counts()
target = target[target >= 1].index
relevant = {x:i for i, x in enumerate(target)}

phago_bacteria["Value"] = len(relevant)

for p in target:
	#print(phago_bacteria.loc[phago_bacteria['Guest'] == p, 'Value'])
	phago_bacteria.loc[phago_bacteria['Guest'] == p, 'Value'] = relevant[p]

p = phago_bacteria["Value"]
print(len(target))
#print(p)
'''
centroid = {}

data_philo = matrix[phago_bacteria.loc[phago_bacteria['Guest'] == 'Proteobacteria'].index]
for philo in target:
	print(philo)
	print(phago_bacteria.loc[phago_bacteria['Guest'] == philo].index)
	data_philo = matrix[phago_bacteria.loc[phago_bacteria['Guest'] == philo].index]
	som_cordenades = [som.winner(x) for x in data_philo]
	centroid[philo] = [np.mean([x for (x,_) in som_cordenades]), np.mean([y for (_,y) in som_cordenades])]
print(centroid)

for x in target:
	w = centroid[x]
	plt.text(w[0]+np.random.rand()*.5, w[1]+np.random.rand()*.5,x)
'''

colors = ["C"+str(i) for i in range(0,len(relevant))]
markers = ["8","s","p",".","o","v","^","<",">","1","2","3","4","P","*","h","H","+","x","X","D","d",1,2,3,4,5,6,7,8,9,10,11]

for cnt, xx in enumerate(matrix):
    w = som.winner(xx)  # getting the winner
    #print(p[cnt])
    #print(colors[p[cnt]])
    # palce a marker on the winning position for the sample xx
    #plt.plot(w[0]+.5, w[1]+.5, markers[p[cnt]], markerfacecolor='None',
    #         markeredgecolor=colors[p[cnt]], markersize=34, markeredgewidth=2)
    #plt.plot(w[0]+.5, w[1]+.5,color=colors[p[cnt]])
    plt.scatter(w[0]+np.random.rand()*.5, w[1]+np.random.rand()*.5, color=colors[p[cnt], loc='upper'])
'''
label = phago_bacteria['Guest']
labels_map = som.labels_map(matrix, label)
label_names = np.unique(label)

plt.figure(figsize=(7, 7))
the_grid = GridSpec(7, 7)
for position in labels_map.keys():
    label_fracs = [labels_map[position][l] for l in label_names]
    plt.subplot(the_grid[6-position[1], position[0]], aspect=1)
    patches, texts = plt.pie(label_fracs)
plt.legend(patches, label_names, bbox_to_anchor=(0, 1.5), ncol=3)
#plt.savefig('resulting_images/som_iris_pies.png')
#plt.show()


plt.axis([0, 6, 0, 6])
plt.savefig('/Users/andressacre/Documents/Universidad/Investigación_Thomas/SOM_prove.png')
plt.show()
'''

#plt.plot([1, 2, 3, 4], [1, 4, 9, 16], 'ro')

plt.show()



