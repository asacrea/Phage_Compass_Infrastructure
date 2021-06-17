#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 07:09:20 2020

@author: andressacre
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

from sklearn.datasets import fetch_mldata
#from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns

input_m = "/Users/andressacre/Documents/Universidad/Investigación_Thomas/Data/Data.tsv"
input_t = "/Users/andressacre/Documents/Universidad/Investigación_Thomas/Data/Taxonomies.tsv"

matrix = pd.read_csv(input_m, sep='\t')
matrix = matrix.to_numpy()

phago_bacteria = pd.read_csv(input_t, sep='\t')

randomlist = random.sample(range(0, 7593), 500)

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

X_embedded = TSNE(n_components=2).fit_transform(matrix)
X_embedded.shape

X_embedded[:,0]
matrix['tsne-2d-one'] = X_embedded[:,0]
matrix['tsne-2d-two'] = X_embedded[:,1]
plt.figure(figsize=(16,10))
sns.scatterplot(
    x="tsne-2d-one", y="tsne-2d-two",
    hue="y",
    palette=sns.color_palette("hls", 10),
    data=matrix,
    legend="full",
    alpha=0.3
)
