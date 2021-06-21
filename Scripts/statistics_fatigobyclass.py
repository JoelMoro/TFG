"""
Program: statistics_fatigobyclass.py
Description: Obtains general statistics for fatiGO according to class taxonomy.
"""

import os

taxfile = "/home/joelmoro/MN/jmoro/protists/initial_data/taxonomy.txt"
cefile = "/home/joelmoro/MN/jmoro/protists/FatiGo_Jaime/fatigo_CE_list.txt"
vefile = "/home/joelmoro/MN/jmoro/protists/FatiGo_Jaime/fatigo_VE_list.txt"
hgtfile = "/home/joelmoro/MN/jmoro/protists/FatiGo_Jaime/fatigo_HGT_list.txt"
cefiledet = "/home/joelmoro/MN/jmoro/protists/FatiGo_Jaime/fatigo_CEdet_list.txt"
vefiledet = "/home/joelmoro/MN/jmoro/protists/FatiGo_Jaime/fatigo_VEdet_list.txt"
hgtfiledet = "/home/joelmoro/MN/jmoro/protists/FatiGo_Jaime/fatigo_HGTdet_list.txt"
aicfile = "/home/joelmoro/MN/jmoro/protists/FatiGo_Jaime/fatigo_AllinCluster_list.txt"


classes = set()
Species_Class = {}
Class_Species = {}
with open(taxfile) as f:
    for line in f:
        line = line.split("\t")
        sps = line[1]
        clas = line[8]
        Species_Class[sps] = clas
        if clas not in Class_Species:
            Class_Species[clas] = set()
        Class_Species[clas].add(sps)



for fn in [cefile, vefile, hgtfile, cefiledet, vefiledet, hgtfiledet, aicfile]:
    print("Stats by class for", fn[53:-9], ":")
    ClassByCount = {}
    total = 0
    with open(fn) as f:
        for line in f:
            sps = line[:5]
            if Species_Class[sps] not in ClassByCount:
                ClassByCount[Species_Class[sps]] = 1
            else:
                ClassByCount[Species_Class[sps]] += 1
            total += 1
    suma = 0
    for c in ClassByCount:
        print("\tPercentage of",c,"-->", (ClassByCount[c]/total)*100 )

