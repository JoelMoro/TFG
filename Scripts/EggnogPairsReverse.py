"""
Program: EggnogPairs.py
Description: Obtain percentage of pairs present in eggnog that are present also in our clusters.
"""

import os, gzip, itertools


def read_pairs(file, translator):
    """
    Reads and translates the pairs of homologs from the files.
    """
    pairs = []
    with gzip.open(file,'rt') as f:
        for line in f:
            line = line.split()
            #Get it translated
            if line[2] in translator and line[3] in translator:
                ProtPair = {translator[line[2]], translator[line[3]]}
                pairs.append(ProtPair)
    return pairs

def read_tsv(file):
    """
    Reads the tsv from eggnog. Takes a little bit long, probably because it is needed to clean
    a little bit each entry to get only the id.
    """

    FamsByProt = {}
    count = 0
    with open(file) as f:
        for line in f:
            count += 1
            line = line.replace("\t", " ").replace(",", " ").split()
            y = int(line[3])
            orthogroup = line[4:-y]
            cleangroup = []
            group_number = line[-y:]
            for num in group_number:
                for prot in orthogroup:
                    if num in prot:
                        prot = prot[len(num)+1:]
                        cleangroup.append(prot)
                        FamsByProt[prot] = str(count)

    return FamsByProt

#Paths when linked to personal computer

tsv_file = "/home/joelmoro/MN/jmoro/protists/eggnog/2759_members.tsv"
pairs_dir = "/home/joelmoro/MN/jmoro/protists/evolclust/pairs_files/"
map_directory = "/home/joelmoro/MN/jmoro/protists/eggnog/maps/"
proteomes_dir = "/home/joelmoro/MN/jmoro/protists/initial_data/proteomes/"



MySps = ["APHIN", "LEIPA"]
#Just to avoid repeating already done comparisons (e.g: APHINvsLEAPI and LEAPIvsAPHIN)
Visited = {}
for sps in MySps:
    Visited[sps] = []



#Get the translation of our dictionary using the mapping files
print("Saving dictionary...")
Translator = {}
for fn in os.listdir(map_directory):
    with open(map_directory+fn) as f:
        for line in f:
            line = line.replace("\t", " ").split()
            Translator[line[0]] = line[1]

#Get all Ids
MySpsId = set()
for fn in os.listdir(proteomes_dir):
    if fn[:-3] in MySps:
        with open(proteomes_dir+fn) as f:
            for line in f:
                if ">" in line:
                    MySpsId.add(Translator[line[1:-1]])
print("Number of ids", len(MySpsId))

#Get all the pairs of our species while translating
MyPairs = {}
print("Getting Pairs...")
for sps in os.listdir(pairs_dir):
    if sps in MySps:
        for fn in os.listdir(pairs_dir+sps+"/"):
            if fn[:-7] in MySps and fn[:-7] not in Visited[sps]:
                Visited[sps].append(fn[:-7])
                Visited[fn[:-7]].append(sps)
                MyPairs[sps+"_x_"+fn[:-7]] = read_pairs(pairs_dir+sps+"/"+fn, Translator)


#Get tsv orthogroups all 
print("Reading Tsv...")
ProtByFam = read_tsv(tsv_file)

#Create eggngo pairs (or groups)

ProtByFamReduced = {}
print("Creating Reduced Tsv...")
for prot in ProtByFam:
    if prot in MySpsId:
        ProtByFamReduced[prot] = ProtByFam[prot]
print("Number of proteins after reduction", len(ProtByFamReduced))

#Reversing and creating pairs:
print("Reversing and creating pairs...")
fams = set(ProtByFamReduced.values())
RevRedTsv = {}
for f in fams:
    RevRedTsv[f] = [prot for prot in ProtByFamReduced if ProtByFamReduced[prot] == f]
print("Reversed!")
TsvPairs = list()
for fam in RevRedTsv:
    if len(RevRedTsv[fam]) > 2:
        for s in itertools.combinations(RevRedTsv[fam], 2):
            TsvPairs.append(set(s))



#Removing solo Pairs, which indeed are not pairs xd.
print("Removing solo pairs")
for Pairs in MyPairs:
    for pair in MyPairs[Pairs]:
        if len(pair) == 1:
            MyPairs[Pairs].remove(pair)

CommonPair = 0
visited = []
print("Total number of pairs in Tsv of our species of interest",len(TsvPairs))
for Pairs in MyPairs:
    print(Pairs, len(MyPairs[Pairs]))
    for pair in MyPairs[Pairs]:
        for pair2 in TsvPairs :
            if pair == pair2 and pair2 not in visited:
                visited.append(pair2)
                CommonPair += 1
print("Number of pairs in common:", CommonPair)                


