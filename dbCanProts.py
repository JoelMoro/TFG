"""
Program: dbCanProts.py
Description: Obtan number of proteins matching with db can results
"""

import os

#Paths
dbdir = "/home/joelmoro/MN/jmoro/protists/dbCanResults/"
clustfile = "/home/joelmoro/MN/jmoro/protists/evolclust/cluster_families.complemented.txt"


cluster_dic = {}
num_of_clusts = 0
with open(clustfile) as f:
    for line in f:
        line = line.replace(";", " ").strip().split()
        if "#" in line:
            current_cluster = line[1]
            num_of_clusts += 1        
        for prot in line[1:]:
            if prot not in cluster_dic:
                cluster_dic[prot] = current_cluster

dbprots = set()
clustfile = "/home/joelmoro/MN/jmoro/protists/evolclust/cluster_families.complemented.txt"
for fn in os.listdir(dbdir):
    if "overview" in fn:
        print("Reading file", fn)
        with open(dbdir+fn) as f:
            for line in f:
                line = line.strip().split()
                if line[0] != "Gene" and line[0] not in dbprots:
                    dbprots.add(line[0])

DB_clusters = {}
no_clusters = set()
for prot in dbprots:
    if prot in cluster_dic:
        DB_clusters[prot] = cluster_dic[prot]
    else:
        no_clusters.add(prot)

print(len(no_clusters))
print(len(DB_clusters))
inv_DB_clusters = {}
for prot in DB_clusters:
    if DB_clusters[prot] not in inv_DB_clusters:
        inv_DB_clusters[DB_clusters[prot]] = {prot}
    else:
        inv_DB_clusters[DB_clusters[prot]].add(prot)

for clid in inv_DB_clusters:
    print(clid, len(inv_DB_clusters[clid]))
print(len(inv_DB_clusters), num_of_clusts)

            





