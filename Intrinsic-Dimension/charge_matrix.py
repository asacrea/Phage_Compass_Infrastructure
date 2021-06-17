import pandas as pd
import numpy as np


df = pd.read_csv("../../Data/nucleotide_dereplicated.tsv", sep='\t')
df = df.fillna(1)

df.to_csv('clean_nucleotide_dereplicated.tsv', sep='\t', header=False, index=False)

df_2 = pd.read_csv("/Users/andressacre/Documents/Universidad/Investigación_Thomas/Code/Intrinsic-Dimension/clean_nucleotide_dereplicated.tsv", sep='\t', header = None)

zero_one_two = [n%9398 for n in range(0,88322404)]
hola = zero_one_two[0:20000]
df_pivot = pd.melt(df_2)
df_pivot.insert(0, 'variable_1', zero_one_two)

df_pivot.to_csv('pivote_nucleotide_dereplicated.tsv', sep='\t', header=False, index=False)

A = np.array([(0, 0.3, 0.4, 0.7),
               (0.3, 0, 0.9, 0.2),
               (0.4, 0.9, 0, 0.1),
               (0.7, 0.2, 0.1, 0)
               ])*10