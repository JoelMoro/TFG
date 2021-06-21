first = True
undec_clusts = set()
total_clusters = 0
path_detailed = "/home/joelmoro/MN/jmoro/protists/MyEvolclust/results_detailed/"
goterms_file = "/home/joelmoro/MN/jmoro/protists/FatiGo_Jaime/mainGOlist.txt"
annot_path = "/home/joelmoro/MN/jmoro/protists/interpro_outs/Annotation/"
with open("/home/joelmoro/MN/jmoro/protists/MyEvolclust/results/evolclassifier.results.txt") as f:
    for line in f:
        if not first:
            line = line.strip().split()
            total_clusters += 1
            if line[-1] == "Undecided":
                undec_clusts.add(line[0])
        else:
            first = False
print(len(undec_clusts))

undecided_hgt = {}
for cluster in undec_clusts:
    with open(path_detailed+cluster+"/evolclassifier.recount.txt") as f:
        undecided_hgt[cluster] = set()
        for line in f:
            line = line.strip().split()
            if "HGT" in line:
                undecided_hgt[cluster].add(line[0])
    if not undecided_hgt[cluster]:
        undecided_hgt.pop(cluster)
print(len(undecided_hgt))

#Statistics for species hgt

