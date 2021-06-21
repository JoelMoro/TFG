"""
Program: tree_0_to_all.py
Description: Little code that appends tree 0 to all_trees.txt file.
"""
import os

all_trees = "/home/joelmoro/MN/jmoro/protists/MyEvolclust/all_trees.txt"
zero_tree = "/home/joelmoro/MN/jmoro/protists/MyEvolclust/0.tree.ml.nw"

tree = ""
#Read 0
print("Reading file 0")
with open(zero_tree) as f:
    for line in f:
        tree += line

#Append in all
with open(all_trees, "a") as f:
    f.write("0"+" "+tree)


