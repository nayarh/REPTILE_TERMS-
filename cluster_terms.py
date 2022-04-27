# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 15:07:28 2022

@author: nayar


"""
import numpy
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from scipy.spatial.distance import pdist
import pandas as pd
import matplotlib.pyplot as plt
import os.path
import pickle




if os.path.isfile("pandas_df"):
    infile = open("pandas_df",'rb')
    mat_pd = pickle.load(infile)
    infile.close()


    plt.figure(figsize=(10, 7))
    plt.title("Dendrograms")
    species = mat_pd
    mat_pd_T = mat_pd.T

    c_dist = pdist(mat_pd_T) # computing the distance
    c_link = linkage(mat_pd_T,  metric='euclidean', method='complete')# computing the linkage
    t = 0.7*max(c_link[:,2])
    clusters = fcluster(c_link, t)
    print(clusters)




    B=dendrogram(c_link)
    plt.show()
else:

    with open("reptile_terms.csv", "r", encoding='cp1252') as terms:
        lines = terms.readlines()

    abb_terms=set()
    abb_terms_2 = set()

    #putting abbreviations and terms into one set to remove repetitions
    for t in lines:


        abb_terms.add((t.split(',')[0], t.split(',')[1]))


    abb_terms = list(abb_terms)


    #Sparse Matrix
    mat = [None] * len(abb_terms)



    #read from reptile database
    with open("reptile_database_2021_11.txt", encoding="utf_16") as f:
        species_list = []
        for line in f.readlines():

            s = line.split("\t")
            species_name = s[1] + " " + s[2]
            species_list.append(species_name)
            for a in abb_terms:



                #cross checking
                if a[0] in line or a[1] in line:

                    if mat[abb_terms.index(a)] is not None:
                        mat[abb_terms.index(a)].append(species_name)



                    else:
                        mat[abb_terms.index(a)] = []
                        mat[abb_terms.index(a)].append(species_name)








    mat_np = numpy.zeros(shape=(len(abb_terms), len(species_list)))
    for i in range(len(mat)):
        if mat[i]:
            for specie in mat[i]:
                mat_np[i][species_list.index(specie)] = 1

    mat_pd = pd.DataFrame(mat_np,columns=species_list, index=abb_terms)

    outfile = open("pandas_df",'wb')
    pickle.dump(mat_pd,outfile)
    outfile.close()
