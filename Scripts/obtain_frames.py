"""
Program: obtain_frames.py
Description: Retrieves a files containing the frames for each proteins extracted from gff files
"""
import os

gff_dir = "/home/joelmoro/MN/jmoro/protists/initial_data/gff/"
strand = {}
for fn in os.listdir(gff_dir):
    print("Reading file:", fn)
    with open(gff_dir+fn) as f:
        for line in f:
            line = line.strip().split("\t")
            strand[line[0]] = line[-1]
of = open("/home/joelmoro/MN/jmoro/protists/MyEvolclust/all_strands.txt", "w")
for prot in strand:
    print(prot+"\t"+strand[prot],file=of)
of.close()

