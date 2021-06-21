"""
Program: ce_clusters.py

Description: Obtains clusters from detailed perspective with only convergent evolution families.
Also little review on percentages for every evolutionary pattern
"""

#Paths
path_detailed = "/home/joelmoro/MN/jmoro/protists/MyEvolclust/results_detailed/"
goterms_file = "/home/joelmoro/MN/jmoro/protists/FatiGo_Jaime/mainGOlist.txt"
annot_path = "/home/joelmoro/MN/jmoro/protists/interpro_outs/Annotation/"

#Obtain percentages for all the evolutionary patterns
first = True
ce_clusts = set()
ve_clusts = set()
un_clusts = set()
total_clusters = 0
with open("/home/joelmoro/MN/jmoro/protists/MyEvolclust/results/evolclassifier.results.txt") as f:
    for line in f:
        if not first:
            line = line.strip().split()
            total_clusters += 1
            if line[-1] == "CE":
                ce_clusts.add(line[0])
            elif line[-1] == "VE":
                ve_clusts.add(line[0])
            elif line[-1] == "Undecided":
                un_clusts.add(line[0])
        else:
            first = False

#Print percentages in console
print(len(ce_clusts), total_clusters, (len(ce_clusts)/total_clusters)*100, "%")
print(len(ve_clusts), total_clusters, (len(ve_clusts)/total_clusters)*100, "%")
print(len(un_clusts), total_clusters, (len(un_clusts)/total_clusters)*100, "%")

#Get specific ce families in the ce clusters.goterms_file
uwu = []
owo = []
for cluster in un_clusts:
    with open(path_detailed+cluster+"/evolclassifier.recount.txt") as f:
        HGT = False
        CE = False
        for line in f:
            line = line.strip().split()
            if "CE" in line:
                CE = True
            if "HGT" in line:
                HGT = True
        if CE:
            uwu.append(cluster)
        if HGT:
            owo.append(cluster)
print(len(uwu), len(owo))


#load go terms
goterms = {}
with open(goterms_file) as f:
    for line in f:
        line = line.strip().split()
        goterms[line[0]] = line[1]

#Get specific ce families in the ce clusters.goterms_file
only_ce_species = {}
for cluster in ce_clusts:
    with open(path_detailed+cluster+"/evolclassifier.recount.txt") as f:
        only_ce_species[cluster] = set()
        for line in f:
            line = line.strip().split()
            if "CE" in line and len(line) == 2:
                only_ce_species[cluster].add(line[0])

#Obtain specific proteins present in families evolving specifically by convergent evolution.
only_ce_prots = {}
missing_set = set()
for cluster in only_ce_species:
    print("Cluster", cluster, "Species that evolved by CE:")
    with open(path_detailed+cluster+"/cluster_family.txt") as f:
        for line in f:
            line = line.replace(";", " ").split()
            if line[0] in  only_ce_species[cluster]:
                print(line[0])
                for prot in line[1:]:
                    if prot in goterms:
                        only_ce_prots[prot] = goterms[prot]
                        print(goterms[prot])
                    else: 
                        missing_set.add(prot)