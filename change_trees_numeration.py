"""
Program: Change_trees_numeration
Description: Fix numeration on the summary file containing all trees
"""

import os

#Path to file
all_trees_file = "/home/joelmoro/MN/jmoro/protists/MyEvolclust/all_trees.txt"

tree_dic = {}
with open(all_trees_file) as f:
    for line in f:
        line = line.split()
        print("Tree", line[0], "Now modified to", str(int(line[0])+1))
        tree_dic[str(int(line[0])+1)] = line[1]
of = open("/home/joelmoro/MN/jmoro/protists/MyEvolclust/all_trees_modified.txt", "w")
for tree in tree_dic:
    print(tree+"\t"+tree_dic[tree],file=of)
of.close()