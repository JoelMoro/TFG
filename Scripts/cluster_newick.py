"""
Program: cluster_newick.py

Description: Obtains each individual reduced species tree regarding the species involved in each cluster
"""

from ete3 import PhyloTree, TreeStyle, faces, NodeStyle, AttrFace, TreeNode
import os

tree_dir = "/home/joelmoro/MN/jmoro/protists/MyEvolclust"
sp100 = PhyloTree(tree_dir + "/ConcatenationSp100.fasta.treefile")
cluster_file = tree_dir+"/cluster_families.complemented.txt"

#Obtain species present in each cluster
with open(cluster_file) as f:
    species = {}
    for line in f:
        line = line.strip().split()
        if "#" in line:
            current_clust = line[1]
            species[current_clust] = []
        else:
            sp = line[0]
            if "_" in sp:
                sp = sp[:-4]
            species[current_clust].append(sp)

#Obtain total species
all_species = []
for n in sp100.get_leaves():
    all_species.append(n.name)
print(all_species)


#Store trees pruning leaves
of = open("/home/joelmoro/MN/jmoro/protists/evolclustdb_inputs/newick_trees_protist.txt", "w")
for cluster in species:
    print(cluster, species[cluster])
    temp_tree = TreeNode(tree_dir + "/ConcatenationSp100.fasta.treefile")
    temp_tree.prune(species[cluster])
    print(cluster+"\t"+temp_tree.write(), file = of)
of.close()


