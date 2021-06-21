"""
Program: evolclass_notree.py
Description: Retrieves clusters and families that do not have tree.
"""

import os

non_verticals = "/home/joelmoro/MN/jmoro/protists/MyEvolclust/Notree_families.txt"
nv_list = []
with open(non_verticals) as f:
    for line in f:
        line = line.strip()
        nv_list.append(line)

notrees =   []
print("getting fams...")
for fam in nv_list:
    print(fam)
    fold = "/home/joelmoro/MN/jmoro/protists/MyEvolclust/results_detailed_notrees/"+fam+"/geneTrees/"
    if not os.listdir(fold):
        notrees.append(fam)

print(len(notrees), notrees)
'''
of = open("/home/joelmoro/MN/jmoro/protists/MyEvolclust/Notree_families.txt", "w")
for fam in notrees:
    print(fam, file = of)
of.close()
'''
        
    