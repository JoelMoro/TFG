"""
Program: interpro_results_analysis.py
Description: Obtains a summary for each category obtainable from interpro:
    - Annotation, Prosite, Pfam and Goterms
"""


import os

#Path for personal computer mount
interpro_path = "/home/joelmoro/MN/jmoro/protists/interpro_outs/"


Pfam = {}
Go = {}
Prosite = {}
Annotation = {}
for fn in os.listdir(interpro_path):
    if ".tsv" in fn:
        print("Reading file:", fn)
        sps = fn[:5]
        Annotation[sps] = {}
        with open(interpro_path+fn) as f:
            for line in f:
                line = line.strip().split("\t")
                if "Pfam" in line:
                    if sps not in Pfam:
                        Pfam[sps] = {}
                    if line[0] not in Pfam[sps]:
                        Pfam[sps][line[0]] = set([])
                    Pfam[sps][line[0]].add(line[4])
                if "ProSitePatterns" in line:
                    if sps not in Prosite:
                        Prosite[sps] = {}
                    if line[0] not in Prosite[sps]:
                        Prosite[sps][line[0]] = set([])
                    Prosite[sps][line[0]].add(line[4])
                if "GO:" in line[-1]:
                    if sps not in Go:
                        Go[sps] = {}
                    if line[0] not in Go[sps]:
                        Go[sps][line[0]] = set([])
                    for gos in line[-1].split("|"):
                        Go[sps][line[0]].add(gos)
                if line[0] not in Annotation[sps]:
                    Annotation[sps][line[0]] = set([])
                Annotation[sps][line[0]].add(line[5])

visited = []
print("Writting in Files Step1")
for sps in Pfam:
    visited.append(sps)
    if sps in Annotation:
        of = open("/home/joelmoro/MN/jmoro/protists/interpro_outs/Annotation/Annot_"+sps+".txt", "w")
        for code in Annotation[sps]:
            for c in Annotation[sps][code]:
                print(code+"\t"+c,file=of)
        of.close()        
    if sps in Go:
        of = open("/home/joelmoro/MN/jmoro/protists/interpro_outs/GoTerms/GO_"+sps+".txt", "w")
        for code in Go[sps]:
            for c in Go[sps][code]:
                print(code+"\t"+c,file=of)
        of.close()
    if sps in Prosite:
        of = open("/home/joelmoro/MN/jmoro/protists/interpro_outs/Prosite/Prosite_"+sps+".txt", "w")
        for code in Prosite[sps]:
            for c in Prosite[sps][code]:
                print(code+"\t"+c,file=of)
        of.close()

    of = open("/home/joelmoro/MN/jmoro/protists/interpro_outs/Pfam/Pfam_"+sps+".txt", "w")
    for code in Pfam[sps]:
        for c in Pfam[sps][code]:
            print(code+"\t"+c,file=of)
    of.close()

#Write in sps not present in pfam
print("Writting in Files Step2")
for sps in Go:
    if sps not in visited:
        visited.append(sps)
        of = open("/home/joelmoro/MN/jmoro/protists/interpro_outs/GoTerms/GO_"+sps+".txt", "w")
        for code in Go[sps]:
            for c in Go[sps][code]:
                print(code+"\t"+c,file=of)
        of.close()
for sps in Prosite:
    if sps not in visited:
        visited.append(sps)
        of = open("/home/joelmoro/MN/jmoro/protists/interpro_outs/Prosite/Prosite_"+sps+".txt", "w")
        for code in Prosite[sps]:
            for c in Prosite[sps][code]:
                print(code+"\t"+c,file=of)        
        of.close()