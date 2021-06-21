"""
Program: hgt_clusters.py
Description: Obtains statistics for hgt specific families and general hgt evolclassifier.
"""


import os
import matplotlib.pyplot as plt 

first = True
hgt_clusts = set()
total_clusters = 0
path_detailed = "/home/joelmoro/MN/jmoro/protists/MyEvolclust/results_detailed/"
goterms_file = "/home/joelmoro/MN/jmoro/protists/FatiGo_Jaime/mainGOlist.txt"
annot_path = "/home/joelmoro/MN/jmoro/protists/interpro_outs/Annotation/"
with open("/home/joelmoro/MN/jmoro/protists/MyEvolclust/results/evolclassifier.results.txt") as f:
    for line in f:
        if not first:
            line = line.strip().split()
            total_clusters += 1
            if line[-1] == "HGT":
                hgt_clusts.add(line[0])
        else:
            first = False

print(len(hgt_clusts), total_clusters, (len(hgt_clusts)/total_clusters)*100, "%")

#load go terms
goterms = {}
with open(goterms_file) as f:
    for line in f:
        line = line.strip().split()
        goterms[line[0]] = line[1]



#Get specific hgt families in the hgt clusters.goterms_file
only_hgt_species = {}
for cluster in hgt_clusts:
    with open(path_detailed+cluster+"/evolclassifier.recount.txt") as f:
        only_hgt_species[cluster] = set()
        for line in f:
            line = line.strip().split()
            if "HGT" in line and len(line) == 2:
                only_hgt_species[cluster].add(line[0])

only_hgt_prots = {}
missing_set = set()
for cluster in only_hgt_species:
    print("Cluster", cluster, "Species that evolved by HGT:")
    with open(path_detailed+cluster+"/cluster_family.txt") as f:
        for line in f:
            line = line.replace(";", " ").split()
            if line[0] in  only_hgt_species[cluster]:
                print(line[0])
                for prot in line[1:]:
                    if prot in goterms:
                        only_hgt_prots[prot] = goterms[prot]
                        print(goterms[prot])
                    else: 
                        missing_set.add(prot)



#Stats for hgt_clusters (same as cluster statistics)

def read_clusterfile(file, hgt_clust):
    ClustDic = {}
    Clusters = {}
    with open(file) as f:
        for line in f:
            if "#" in line:
                line = line.split()
                clust_id = line[1]
                Clusters[clust_id] = []
            else:
                line = line.replace(";", " ").split()
                sps = line[0]
                
                if "_" in sps:
                    sps = sps[:-4]
                Clusters[clust_id].append(sps)
                if sps not in ClustDic and clust_id in hgt_clusts:
                    ClustDic[sps] = 1
                elif sps in ClustDic and clust_id in hgt_clusts:
                    ClustDic[sps] += 1
                
    return ClustDic, Clusters



#Personal computer paths
cluster_file = "/home/joelmoro/MN/jmoro/protists/evolclust/cluster_families.complemented.txt"
pairs_path = "/home/joelmoro/MN/jmoro/protists/evolclust/pairs_files/"

#Keep all possible species:
all_species = []
for fn in os.listdir(pairs_path):
    if fn not in all_species:
        all_species.append(fn)

#Number of times each species appears in our clusters:
clustdic, clusters = read_clusterfile(cluster_file, hgt_clusts)



#with which species do species clusterize:
ClustersDistribution = {}
for cluster in clusters:
    #only if the clust is hgt
    if cluster in hgt_clusts:
        for sps in clusters[cluster]:
            if sps not in ClustersDistribution:
                ClustersDistribution[sps] = {}
            for sps2 in clusters[cluster]:
                if sps != sps2:
                    if sps2 not in ClustersDistribution[sps]:
                        ClustersDistribution[sps][sps2] = 1
                    else:
                        ClustersDistribution[sps][sps2] += 1


print(clustdic)
print("The species that appears the most is", max(clustdic, key = clustdic.get), "with a total of",
clustdic[max(clustdic, key = clustdic.get)], "clusters")


plt.bar(list(clustdic.keys()), clustdic.values(), color = "g")   
plt.xticks(rotation = 65)
plt.show()
for sps in ClustersDistribution:
    plt.title(sps)
    plt.bar(list(ClustersDistribution[sps].keys()), ClustersDistribution[sps].values(), color = "g")   
    plt.xticks(rotation = 60)
    plt.show()


