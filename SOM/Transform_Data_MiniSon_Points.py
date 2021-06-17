import dendropy
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.gridspec import GridSpec
from minisom import MiniSom 

input_m = "/Users/andressacre/Data_Matrix/Data.tsv"
input_t = "/Users/andressacre/Data_Matrix/Taxonomies.tsv"

matrix = pd.read_csv(input_m, sep='\t')
matrix = matrix.to_numpy()

phago_bacteria = pd.read_csv(input_t, sep='\t')

som = MiniSom(5, 5, 7593, sigma=0.1, learning_rate=0.2, random_seed=10)
print("Training...")	
som.train_random(matrix, 1000)
print("\n...ready!")

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

p = phago_bacteria["Value"]

colors = ["C"+str(i) for i in range(0,len(relevant)+1)]

plt.figure(figsize=(13, 7))
plt.subplot(121)
for cnt, xx in enumerate(matrix):
    w = som.winner(xx)  # getting the winner
    plt.scatter(w[0]+np.random.rand()*.9, w[1]+np.random.rand()*.9, color=colors[p[cnt]], s=10)

custom_lines = [Line2D([0], [0], color=colors[i], lw=4) for i,t in enumerate(target)]
# Place a legend to the right of this smaller subplot.
#plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
plt.xlabel('X-SOM')
plt.ylabel('Y-SOM')
plt.title('SOM - Phage Structure')
plt.text(2.8, 5.6, r'learning_rate=0.2,\ \sigma=0.1')
plt.grid(True)
plt.legend(custom_lines, target, ncol=3, bbox_to_anchor=(1.05, 1),loc='upper left', borderaxespad=0.)
#plt.axis([0, 6, 0, 6])
plt.savefig('/Users/andressacre/Documents/Universidad/Investigación_Thomas/Results/SOM/SOM_Prove_10.png')
plt.show()

