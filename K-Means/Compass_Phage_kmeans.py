from time import time

import dendropy

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale

np.random.seed(42)

tree = dendropy.Tree.get_from_path("/Users/andressacre/Documents/Universidad/Investigación_Thomas/Data/Feb-Abril/nucleotide_all_vs_all_tree.nwk","newick")
phago_bacteria = pd.read_csv("/Users/andressacre/Documents/Universidad/Investigación_Thomas/Data/Feb-Abril/26Aug2019_phages_hosts.tsv", sep='\t')

n = list(enumerate(tree.taxon_namespace[:]))[len(list(enumerate(tree.taxon_namespace[:])))-1][0]

matrix = np.load("/Users/andressacre/Documents/Universidad/Investigación_Thomas/Data/Feb-Abril/matrix.npy")


input_f = "/Users/andressacre/Documents/Universidad/Investigación_Thomas/Code/Intrinsic-Dimension/clean_nucleotide_dereplicated.tsv"
f1 = open(input_f)
data = []
for line in f1:
    data.append([float(x) for x in line.split()])

#X_digits, y_digits = load_digits(return_X_y=True)
data = matrix

#Get different guest of pheges with frequency > 20 
target = phago_bacteria['Guest'].value_counts()
target = target[target >= 20].index

#Get enumerate dictironary to each one guest
relevant = {x:i for i, x in enumerate(target)}

phago_bacteria["Value"] = len(relevant)
for p in target:
  phago_bacteria.loc[phago_bacteria['Guest'] == p, 'Value'] = relevant[p]

target = list(target)
target.append("Others")

p = phago_bacteria["Value"]

n_samples, n_features = data.shape
n_digits = len(relevant)
labels = target

sample_size = 300

print("n_digits: %d, \t n_samples %d, \t n_features %d"
      % (n_digits, n_samples, n_features))

# in this case the seeding of the centers is deterministic, hence we run the
# kmeans algorithm only once with n_init=1
pca = PCA(n_components=n_digits).fit(data)
features = range(pca.n_components_)

plt.bar(features, pca.explained_variance_)
plt.xticks(features)
plt.ylabel('Variance')
plt.xlabel('PCA features')
plt.show()

mean = pca.mean_
first_pc = pca.components_[0,:]

plt.arrow(mean[0], mean[1], first_pc[0], first_pc[1], color='red', width=0.01)


plt.plot(np.cumsum(pca.explained_variance_ratio_))
plt.xlabel('number of components')
plt.ylabel('cumulative explained variance');





# #############################################################################
# Visualize the results on PCA-reduced data

reduced_data = PCA(n_components=2).fit_transform(data)
kmeans = KMeans(init='k-means++', n_clusters=n_digits, n_init=10)
kmeans.fit(reduced_data)

# Step size of the mesh. Decrease to increase the quality of the VQ.
h = .02     # point in the mesh [x_min, x_max]x[y_min, y_max].

# Plot the decision boundary. For that, we will assign a color to each
x_min, x_max = reduced_data[:, 0].min() - 1, reduced_data[:, 0].max() + 1
y_min, y_max = reduced_data[:, 1].min() - 1, reduced_data[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

# Obtain labels for each point in mesh. Use last trained model.
Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])

# Put the result into a color plot
Z = Z.reshape(xx.shape)
plt.figure(1)
plt.clf()
plt.imshow(Z, interpolation='nearest',
           extent=(xx.min(), xx.max(), yy.min(), yy.max()),
           cmap=plt.cm.Paired,
           aspect='auto', origin='lower')

plt.plot(reduced_data[:, 0], reduced_data[:, 1], 'k.', markersize=2)
# Plot the centroids as a white X
centroids = kmeans.cluster_centers_
plt.scatter(centroids[:, 0], centroids[:, 1],
            marker='x', s=169, linewidths=3,
            color='w', zorder=10)
plt.title('K-means clustering on the BacterioPhages dataset (PCA-reduced data)\n'
          'Centroids are marked with white cross')
plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)
plt.xticks(())
plt.yticks(())
plt.show()