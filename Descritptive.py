import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

phago_bacteria = pd.read_csv("/Users/andressacre/Documents/Universidad/Investigación_Thomas/Data/26Aug2019_phages_hosts.tsv",
	sep='\t')

type_counts = phago_bacteria['Guest'].value_counts()
df2 = pd.DataFrame(type_counts)
print(df2)

type_counts.plot.pie(y='Guest')
