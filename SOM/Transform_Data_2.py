import dendropy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def closest_node(data, t, map, m_rows, m_cols): . .
def euc_dist(v1, v2): . .
def manhattan_dist(r1, c1, r2, c2): . .
def most_common(lst): . .

def main():
  # 0. get started
  np.random.seed(1)
  Dim = 4
  Rows = 30; Cols = 30
  RangeMax = Rows + Cols
  LearnMax = 0.5
  StepsMax = 5000

  # 1. load data into memory
  # 2. construct the SOM
  # 3. construct and display U-Matrix
  # 4. construct and display reduced data

if __name__=="__main__":
  main()

tree = dendropy.Tree.get_from_path("/Users/andressacre/Documents/Universidad/Investigación_Thomas/prove.nwk", "newick")
pdc = tree.phylogenetic_distance_matrix()

matrix = np.zeros((33,33))
index = []
for i, t1 in enumerate(tree.taxon_namespace[:-1]):
	for j, t2 in enumerate(tree.taxon_namespace[i+1:]):
		if((i+j+1)<=32):
			#print("FIla '%s', Coumna ''%s" % (i,i+j+1))
			matrix[i][i+j+1] = pdc(t1,t2)
			#print(matrix[i][j])
			#print("Distance between '%s' and '%s': %s" % (t1.label, t2.label, pdc(t1, t2)))
		
	index.append(t1.label)

table2 = pd.DataFrame(matrix, index=index, columns=index)
'''
print(matrix)
print(matrix[0][2])

print(tree.taxon_namespace[0].label)
print(tree.taxon_namespace[2].label)
print(pdc(tree.taxon_namespace[0], tree.taxon_namespace[2]))
'''

print("Constructing a 30x30 SOM from the iris data")
map = np.random.random_sample(size=(Rows,Cols,Dim))


for s in range(StepsMax):
    if s % (StepsMax/10) == 0: print("step = ", str(s))
    pct_left = 1.0 - ((s * 1.0) / StepsMax)
    curr_range = (int)(pct_left * RangeMax)
    curr_rate = pct_left * LearnMax

    t = np.random.randint(len(data_x))
    (bmu_row, bmu_col) = closest_node(data_x, t, map, Rows, Cols)

    for i in range(Rows):
      for j in range(Cols):
        if manhattan_dist(bmu_row, bmu_col, i, j) < curr_range:
          map[i][j] = map[i][j] + curr_rate *
         (data_x[t] - map[i][j])





    