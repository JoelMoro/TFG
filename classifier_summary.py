"""
Program: classifier_summary.py
Description: Obtain a file summarizing the different detailed patterns found in families for each
of the conserved gene clusters under study.
"""


import os

#Keep all the patterns identified in each cluster 
status = {}
results_detailed = "/home/joelmoro/MN/jmoro/protists/MyEvolclust/results_detailed/"
for fn in os.listdir(results_detailed):
    print("Reading cluster:", fn)
    with open(results_detailed+fn+"/evolclassifier.final_table.txt") as f:
        status[fn] = [] 
        for line in f:
            line = line.replace("\t", " ").split()
            if "Undecided" in line and "Undecided" not in status[fn]:
                status[fn].append("Undecided")
            if "VE" in line and "VE" not in status[fn]:
                status[fn].append("VE")
            if "CE" in line and "CE" not in status[fn]:
                status[fn].append("CE")
            if "Unrelated" in line and "Unrelated" not in status[fn]:
                status[fn].append("Unrelated")
            if "HGT" in line and "HGT" not in status[fn]:
                status[fn].append("HGT")

print("Writting summary...")
with open("/home/joelmoro/MN/jmoro/protists/MyEvolclust/results_detailed_resume.txt", "w") as f:   
    for cl in status:
        f.write(cl+"\t")
        for st in status[cl]:
            f.write(st+" ")
        f.write("\n")
