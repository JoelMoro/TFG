"""
Program: getfatigo_lists.py
Description: Obtains the different lists that are used as input for FatiGO, aswell as the 
template list regarding the full list of proteins that is used also as input for fatiGO.
"""

import os

resdet_file = "/home/joelmoro/MN/jmoro/protists/MyEvolclust/results_detailed_resume.txt"
res_file = "/home/joelmoro//MN/jmoro/protists/MyEvolclust/results/evolclassifier.results.txt"
detail_path = "/home/joelmoro/MN/jmoro/protists/MyEvolclust/results_detailed/"
cluster_file = "/home/joelmoro/MN/jmoro/protists/evolclust/cluster_families.complemented.txt"

HGT_clusters_det = ["HGTdet"]
CE_clusters_det = ["CEdet"]
VE_clusters_det = ["VEdet"]


with open(resdet_file) as f:
    for line in f:
        line = line.strip().split()
        if "HGT" in line:
            HGT_clusters_det.append(line[0])
        if "CE" in line:
            CE_clusters_det.append(line[0])
        if "VE" in line:
            VE_clusters_det.append(line[0])

HGT_clusters = ["HGT"]
CE_clusters = ["CE"]
VE_clusters = ["VE"]

with open(res_file) as f:
    for line in f:
        line = line.strip().split()
        if "HGT" in line and "#ClName" not in line: 
            HGT_clusters.append(line[0])
        if "CE" in line and "#ClName" not in line:
            CE_clusters.append(line[0])
        if "VE" in line and "#ClName" not in line:
            VE_clusters.append(line[0])


print("Reading all Clusters ...")

AllClusters = {}
with open(cluster_file) as f:
    for line in f:
        line = line.strip().replace(";", " ").split()
        if "#" in line:
            clustid = line[1]
            AllClusters[clustid] = set()
        else:
            for prot in line:
                AllClusters[clustid].add(prot)

print("Saving proteins for default results...")
for clust in [HGT_clusters, VE_clusters, CE_clusters]:
    prots = set()
    print("Reading", clust[0])
    for cl in clust[1:]:
        for prot in AllClusters[cl]:
            if prot not in prots:
                prots.add(prot)

    print("Writting list", clust[0])
    of = open("/home/joelmoro/MN/jmoro/protists/FatiGo_Jaime/fatigo_"+clust[0]+"_list.txt", "w")
    for prot in prots:
        print(prot,file=of)
    of.close()

print("Saving proteins for detailed results...")
for clust in [HGT_clusters_det, VE_clusters_det, CE_clusters_det]:
    species = []
    prots = []
    print("Reading", clust[0])
    for cl in clust[1:]:
        clustfam_file = detail_path+cl+"/cluster_family.txt"
        with open(clustfam_file) as f:
            for line in f:
                line = line.strip().replace(";", " ").split()
                if "#" not in line and line[0] not in species:
                    sps = line[0]
                    if "_" in line[0]:
                        sps = line[0][:-4]
                    species.append(sps)
                    for p in line[1:]:
                        if p not in prots:
                            prots.append(p)

    print("Writting list", clust[0])
    of = open("/home/joelmoro/MN/jmoro/protists/FatiGo_Jaime/fatigo_"+clust[0]+"_list.txt", "w")
    for prot in prots:
        print(prot,file=of)
    of.close()

print("Saving all proteins in cluster...")
prots = set()
for clust in AllClusters:
    for prot in AllClusters[clust]:
        if prot not in prots:
            prots.add(prot)
print("Writting All prots in cluster list")
of = open("/home/joelmoro/MN/jmoro/protists/FatiGo_Jaime/fatigo_AllinCluster_list.txt", "w")
for prot in prots:
    print(prot,file=of)
of.close()


print("Reading all proteomes...")
all_prots = []
proteomes = "/home/joelmoro/MN/jmoro/protists/initial_data/proteomes/"
for fn in os.listdir(proteomes):
    if ".fa" in fn:
        with open(proteomes+fn) as f:
            for line in f:
                line = line.strip().split()
                if ">" in line[0]:
                    all_prots.append(line[0][1:]) 
                


print("Writting all prots list...")
of = open("/home/joelmoro/MN/jmoro/protists/FatiGo_Jaime/fatigo_allprots.txt", "w")
for prot in all_prots:
    print(prot,file=of)
of.close()