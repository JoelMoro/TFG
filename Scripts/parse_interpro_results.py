#!/usr/bin/env python

#Parse interproscan results:

strains = ["B1012M","BG2","CBS138","CST110","CST35","EB0911Sto","EF1237Blo1","M12","M6","M7","P35-2","SAT_BAL01","Cg16","Cg17","Cg19","Cg21","Cg25","Cg28","Cg30","DSY562","DSY565"]

import glob

for fileName in glob.glob("interpro/*tsv"):
    strain = fileName.split("/")[-1].split(".")[0]
    omit = False
    if strain in strains:
        a = 5
        g = 13
        p = 4
    else:
        if "modified" in fileName:
            a = 6
            g = 14
            p = 5
        else:
            omit = True
    if not omit:
        info = {}
        GOs = {}
        Pfam = {}
        for line in open(fileName):
            line = line.strip()
            dades = line.split("\t")
            if dades[0] not in info:
                info[dades[0]] = set([])
            info[dades[0]].add(dades[a])
            if "Pfam" in line:
                if dades[0] not in Pfam:
                    Pfam[dades[0]] = set([])
                Pfam[dades[0]].add(dades[p])
            if "GO:" in line:
                if dades[0] not in GOs:
                    GOs[dades[0]] = set([])
                for gos in dades[g].split("|"):
                    GOs[dades[0]].add(gos)
        outfile = open("annotations/"+strain+".txt","w")
        for code in info:
            print(code+"\t"+";".join(list(info[code])),file=outfile)
        outfile.close()
        outfile = open("GO_terms/"+strain+".txt","w")
        for code in GOs:
            for c in GOs[code]:
                print(code+"\t"+c,file=outfile)
        outfile.close()
        outfile = open("Pfams/"+strain+".txt","w")
        for code in Pfam:
            for c in Pfam[code]:
                print(code+"\t"+c,file=outfile)
        outfile.close()
