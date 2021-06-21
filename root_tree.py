"""
Program: root_tree.py
Description: Little piece of code used to root the species tree.
"""
from ete3 import PhyloTree, Tree

t = PhyloTree("/home/joelmoro/MN/jmoro/protists/MyEvolclust/ConcatenationSp100.fasta.treefile")
m = t.get_midpoint_outgroup()
t.set_outgroup(m)
t.write(format=1, outfile="rooted_species_tree.nw")