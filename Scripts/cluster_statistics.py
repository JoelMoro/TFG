"""
Program: cluster_statistics.py
Descrpition: Obtain distributions (general and specific) of the association between
species aswell as numeric interesting statistics as the most present species, or the species
with the highest number of association with different species.
"""

import os
import matplotlib.pyplot as plt


def read_clusterfile(file):
    """
    Retrieves: 
        - total number of proteins, the total number of cluster families.
        - Dictionary with species as key and the number of times appearing 
        in cluster as value.
        - Dictionary with cluster id as key and the species appearing in the cluster
        as value.
    """

    ClustDic = {}
    Clusters = {}
    with open(file) as f:
        total_prots = 0
        cluster_families = 0
        for line in f:
            if "#" in line:
                line = line.split()
                clust_id = line[1]
                Clusters[clust_id] = []
            else:
                line = line.replace(";", " ").split()
                sps = line[0]
                cluster_families += 1
                total_prots += len(line)-1
                if "_" in sps:
                    sps = sps[:-4]
                Clusters[clust_id].append(sps)
                if sps not in ClustDic:
                    ClustDic[sps] = 1
                else:
                    ClustDic[sps] += 1
                
    return ClustDic, Clusters, total_prots, cluster_families



#Personal computer paths
cluster_file = "/home/joelmoro/MN/jmoro/protists/evolclust/cluster_families.complemented.txt"
pairs_path = "/home/joelmoro/MN/jmoro/protists/evolclust/pairs_files/"

#Keep all possible species:
all_species = []
for fn in os.listdir(pairs_path):
    if fn not in all_species:
        all_species.append(fn)

#Number of times each species appears in our clusters:
clustdic, clusters, total_prots, clus_fam = read_clusterfile(cluster_file)
print("Species appearing in our clusters = ", str(len(clustdic))+".", len(all_species)-len(clustdic), "missing")
print(total_prots, clus_fam)

#Species that do not appear in cluster.s
missing = []
for sps in all_species:
    if sps not in clustdic:
        missing.append(sps)
print("Species missing:", len(missing))
print(missing)

#with which species do species clusterize:
"""
ClustersDistribution = {}
for cluster in clusters:
    for sps in clusters[cluster]:
        if sps not in ClustersDistribution:
            ClustersDistribution[sps] = []
        for sps2 in clusters[cluster]:
            if sps != sps2 and sps2 not in ClustersDistribution[sps]:
                ClustersDistribution[sps].append(sps2)
"""
ClustersDistribution = {}
for cluster in clusters:
    for sps in clusters[cluster]:
        if sps not in ClustersDistribution:
            ClustersDistribution[sps] = {}
        for sps2 in clusters[cluster]:
            if sps != sps2:
                if sps2 not in ClustersDistribution[sps]:
                    ClustersDistribution[sps][sps2] = 1
                else:
                    ClustersDistribution[sps][sps2] += 1

#Species with the biggest number:
max_sps = max(ClustersDistribution, key= lambda sps: len(set(ClustersDistribution[sps])))

print("The species that appears the most is", max(clustdic, key = clustdic.get), "with a total of",
clustdic[max(clustdic, key = clustdic.get)], "clusters")
print("The species that clusterized with the biggest number of species is",  max_sps, "with a total of", 
        len(ClustersDistribution[max_sps]))
print("Number of species associated with NOTSP", len(ClustersDistribution["NOTSP"]))
print(ClustersDistribution["NOTSP"])
plt.bar(list(clustdic.keys()), clustdic.values(), color = "g")   
plt.xticks(rotation = 65)
plt.show()
for sps in ClustersDistribution:
    plt.title(sps)
    plt.bar(list(ClustersDistribution[sps].keys()), ClustersDistribution[sps].values(), color = "g")   
    plt.xticks(rotation = 60)
    plt.show()
