"""
Program: find_pathogenesisCEprots.py
Description: Checks for proteins indentify to evolve by CE associated with pathogenesis
GO terms. Also functions for cellad and sterol biosynthesis are secondarily checked.
"""

import os

golist = "/home/joelmoro/MN/jmoro/protists/FatiGo_Jaime/mainGOlist.txt"
celist = "/home/joelmoro/MN/jmoro/protists/FatiGo_Jaime/fatigo_CE_list.txt"
hgtlist = "/home/joelmoro/MN/jmoro/protists/FatiGo_Jaime/fatigo_HGT_list.txt"
clustfile = "/home/joelmoro/MN/jmoro/protists/evolclust/cluster_families.complemented.txt"
taxfile = "/home/joelmoro/MN/jmoro/protists/initial_data/taxonomy.txt"

pathoprots = set()
cellad_prots = set()
evhost_prots = set()

sterol_prots = set()

with open(golist) as f:
    for line in f:
        line = line.strip().split()
        if line [1] == "GO:0009405":
            pathoprots.add(line[0])
        elif line[1] == "GO:0007155":
            cellad_prots.add(line[0])
        elif line[1] == "GO:0020012" or line[1] == "GO:0042783":
            evhost_prots.add(line[0])
        elif line[1] == "GO:0016126":
            sterol_prots.add(line[0])


cepathos = set()
with open(celist) as f:
    for line in f:
        line = line.strip().split()
        if line[0] in pathoprots:
            cepathos.add(line[0])

hgtsterols = set()
with open(hgtlist) as f:
    for line in f:
        line = line.strip().split()
        if line[0] in sterol_prots:
            hgtsterols.add(line[0])


of = open("/home/joelmoro/MN/jmoro/protists/FatiGo_Jaime/interest_lists/PathoProts_CE.txt", "w")
for prot in cepathos:
    print(prot,file=of)
of.close()

cluster_dic = {}
print("Reading Cluster file")
with open(clustfile) as f:
    for line in f:
        line = line.replace(";", " ").strip().split()
        if "#" in line:
            current_cluster = line[1]        
        for prot in line[1:]:
            if prot not in cluster_dic:
                cluster_dic[prot] = current_cluster


PathoClusters = {}
for prot in cepathos:
    if cluster_dic[prot] not in PathoClusters:
        PathoClusters[cluster_dic[prot]] = [prot]
    else:
        PathoClusters[cluster_dic[prot]].append(prot)
for clid in PathoClusters:
    print("\t"+clid, len(PathoClusters[clid]))
    for prot in PathoClusters[clid]:
        with open ("/home/joelmoro/MN/jmoro/protists/evolclust/conversion_files/"+prot[:5]+".txt") as f:
            for line in f:
                line = line.strip().split()
                if line[0] == prot:
                    print(line[0], line[1])
