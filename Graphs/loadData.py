# -*- coding: utf-8 -*-
#!/usr/bin/python
import sys
import json
import copy
import random
from time import time
import numpy as np
import pandas as pd

class LoadData(object):
    #path files sources
    __instance = None
    input_m = "/Users/andresacre/Data/Phage_Compass/Data.tsv"
    input_t = "/Users/andresacre/Data/Phage_Compass/Taxonomies.tsv"
    l = 0
    n = 0
    flag = False
    matrix_2 = None
    #p = None
    #p_2 = None
    
    def __init__(self,n):
        #print(LoadData.flag)
        #Random subsample
        random.seed(30)
        self.n = n
   
    def makeMatrix(self,upper_threshold = 0, botton_threshold = 0, write = False):
        upper_threshold = 1 - upper_threshold
        botton_threshold = 1 - botton_threshold
        print("Loading matrix")
        #Load data
        print("write inicial: " + str(write))
        #if self.flag:
        print("Hola soy n: " + str(self.n))
        matrix = pd.read_csv(self.input_m, sep='\t', header = None)
        matrix = matrix.to_numpy()
        #Submatrix
        #LoadData.matrix_2 = matrix[self.l[:,None],self.l]
        matrix_2 = matrix[0:self.n:1, 0:self.n:1]
        matrix_2 = 1 - matrix_2 
        
        if(botton_threshold == 0):
            print("Upper threshold " + str(upper_threshold))
            matrix_2[matrix_2 <= upper_threshold] = 0
            name = "prueba_threshold_" + str(upper_threshold)[-1] + "_" +str(self.n) + ".tsv"
        else:
            print("Thresholds entre " + str(botton_threshold) + " y " + str(upper_threshold))
            matrix_2[matrix_2 <= upper_threshold] = 0
            matrix_2[matrix_2 >= botton_threshold] = 0
            name = "prueba_threshold_" + str(upper_threshold)[-1] + "_"+ str(botton_threshold)[-1] + "_" + str(self.n) +".tsv"
        if write:
            np.savetxt("/Users/andressacre/Data_Matrix/"+ name, matrix_2, delimiter="\t")
            print("Escribí")
        LoadData.flag =  False
        print("Matrix loaded")
        
        return matrix_2
    
    def makeP(self): 
        print("Loading Taxonomies of host")
        phago_bacteria = pd.read_csv(self.input_t, sep='\t')
        
        #Get Phyla names
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
        
        #p = phago_bacteria["Value"][self.l]
        p = phago_bacteria["Value"][0:self.n]
        p_2 = list(p.index)
        
        #type_counts = phago_bacteria['Guest'].value_counts()
        #type_counts = phago_bacteria['Value'].value_counts()
        #df2 = pd.DataFrame(type_counts)
        #print(df2)
        #type_counts.plot.pie(y='Guest')
        print("Taxonomies loaded")
        return p, p_2, target
    
    def makeGen(self): 
        print("Loading Taxonomies of host")
        phago_bacteria = pd.read_csv(self.input_t, sep='\t')
        
        #Get Phyla names
        phage_range = range(0,len(phago_bacteria.index))
        genus = [json.loads(phago_bacteria['Host lineage'][i].replace("'","\""))['genus'] for i in phage_range]
        genus = [x[0] for x in genus]
        phago_bacteria["Guest"] = genus
        target = phago_bacteria["Guest"].value_counts()
        target = target[target >= 40].index
        
        relevant = {x:i for i, x in enumerate(target)}
        
        phago_bacteria["Value"] = len(relevant)
        for p in target:
            	phago_bacteria.loc[phago_bacteria['Guest'] == p, 'Value'] = relevant[p]
        
        target = list(target)
        target.append("Others")
        
        #p = phago_bacteria["Value"][self.l]
        p = phago_bacteria["Value"][0:self.n]
        p_2 = list(p.index)
        
        #type_counts = phago_bacteria['Guest'].value_counts()
        #type_counts = phago_bacteria['Value'].value_counts()
        #df2 = pd.DataFrame(type_counts)
        #print(df2)
        #type_counts.plot.pie(y='Guest')
        print("Taxonomies loaded")
        return p, p_2, target
    
    
if __name__ == '__main__':
    l = LoadData()
