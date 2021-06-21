"""
Program: EggnogPairs.py
Description: Obtain percentage of pairs present in our clusters not present in eggnog.
"""


import os, gzip


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
                ProtPair = [translator[line[2]], translator[line[3]]]
                pairs.append(ProtPair)
    return pairs

def read_tsv(file):
    """
    Reads the tsv from eggnog. Takes a little bit long, probably because it is needed to clean
    a little bit each entry to get only the id.
    """
    OrthoGroups = {}
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
            OrthoGroups[str(count)] = cleangroup
    return OrthoGroups, FamsByProt


#Paths when linked to personal computer

tsv_file = "/home/joelmoro/MN/jmoro/protists/eggnog/2759_members.tsv"
pairs_dir = "/home/joelmoro/MN/jmoro/protists/evolclust/pairs_files/"
map_directory = "/home/joelmoro/MN/jmoro/protists/eggnog/maps/"

#Paths from Toni's computer
'''
tsv_file = "/home/jmoro/MN/jmoro/protists/eggnog/2759_members.tsv"
pairs_dir = "/home/jmoro/MN/jmoro/protists/evolclust/pairs_files/"
map_directory = "/home/jmoro/MN/jmoro/protists/eggnog/maps/"
'''
#Paths from MN:
'''
tsv_file = "/gpfs/projects/bsc40/current/jmoro/protists/eggnog/2759_members.tsv"
pairs_dir = "/gpfs/projects/bsc40/current/jmoro/protists/evolclust/pairs_files/"
map_directory = "/gpfs/projects/bsc40/current/jmoro/protists/eggnog/maps/"
'''


MySps = ["APHIN", "AURAN", "BIGNA", "DICPU", "ECTSI", "FONAL", "GALSU", "GIAIN", "GRENI", "GUITH", "ICHMU", "LEIPA", "PHYKE", "PHYSO", "PLABE", "PLAVI", "SALRO", "THAOC", "THEAN"]


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
tsvorto, ProtByFam = read_tsv(tsv_file)

#Check MyPairs
#Maybe with variables for just counting instead of keeping a dictionary of a list is faster? Trying.
present = 0
total = 0
print("Performing comparison...")
z

PresentPairs = {}
NonPresentPairs = {}
for pairs in MyPairs:
    print("Set:", pairs)
    PresentPairs[pairs] = []
    NonPresentPairs[pairs] = []
    for pair in MyPairs[pairs]:
        if pair[0] in ProtByFam and pair[1] in ProtByFam:
            if ProtByFam[pair[0]] == ProtByFam[pair[1]]:
                #print(pair[0], pair[1])
                PresentPairs[pairs].append(pair)
            else:
                NonPresentPairs[pairs].append(pair)

print("Results")
sumP = 0
sumNP = 0
for pairs in PresentPairs:
    if len(PresentPairs[pairs]) != 0 and (NonPresentPairs[pairs] != 0):
        #Present let us know tha pairs contained in Eggnog
        print("Set", pairs, "number of pairs present", len(PresentPairs[pairs]))
        print("Set", pairs, "number of pairs NOT present", len(NonPresentPairs[pairs]))
    sumP += len(PresentPairs[pairs])
    sumNP += len(NonPresentPairs[pairs])
print(sumP/(sumP+sumNP))