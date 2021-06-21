#!/usr/bin/env python
# coding: utf-8

"""
Program: Concatenation.py
Description: Jupyter notebook export used to obtain the concatenations.
"""

# In[2]:


import os
import sys


# In[3]:


current = os.getcwd()


# In[78]:


MyDirs = [current+"/sp80", current+"/sp100Treeko", current+"/sp125Treeko"]
MyDirs


# In[79]:


def get_sequence(file):
    Sequences = {}
    with open(file) as f:
        for line in f:
            if len(line) > 1:
                line = line.strip()
                if line.startswith(">"):
                    seq_name = line[1:]
                    if seq_name not in Sequences:
                        Sequences[seq_name[:5]] = ""
                else:
                    seq = line.replace('\n','')
                    Sequences[seq_name[:5]] += seq
    return Sequences

def isLength(dic):
    mbool = True
    l = []
    for c in dic:
        l.append(len(dic[c]))
    truelen = l[0]
    for seq in l:
        if seq != truelen:
            mbool = False
    if not mbool:
        return "PROBLEM! ORIGINAL SEQ MISSMATCH LENGTH"
    else:
        return "No problem in f_seqs"
        
        


# In[87]:


Concatenations = {}
for MyDir in MyDirs:
    Concatenation = {}
    subdirs , dirs, filenames = next(os.walk(MyDir))
    for sd in dirs:
        _, _, filenames = next(os.walk(MyDir+"/"+sd))
        #First loop
        for f in filenames:
            if "clean.fasta" in f:
                f_seqs = get_sequence(MyDir+"/"+sd+"/"+f)
                for sps in f_seqs:
                    if sps not in Concatenation:
                        Concatenation[sps] = ""

    print(Concatenation)
    #Repeat the loop:
    for sd in dirs:
        _, _, filenames = next(os.walk(MyDir+"/"+sd))
        for f in filenames:
            if "clean.fasta" in f:
                f_seqs = get_sequence(MyDir+"/"+sd+"/"+f)
                for sps in f_seqs:
                    Concatenation[sps] += f_seqs[sps]
                currlen = len(f_seqs[sps])
                for sps in Concatenation:
                    if sps not in f_seqs:
                        Concatenation[sps] += currlen*"-"
                    
    Concatenations[MyDir] = Concatenation
    #Generate concatenated file
    new_file = open(MyDir+"/Concatenation.fasta", "w")
    for sps in Concatenation:
            new_file.write(">"+sps+"\n")
            seq = Concatenation[sps]
            new_file.write(seq+"\n")        
                    


# In[ ]:


MyDir = MyDirs[0]
Concatenation = {}
subdirs , dirs, filenames = next(os.walk(MyDir))
for sd in dirs:
    _, _, filenames = next(os.walk(MyDir+"/"+sd))
    #First loop
    for f in filenames:
         if "clean.fasta" in f:
            f_seqs = get_sequence(MyDir+"/"+sd+"/"+f)
            for sps in f_seqs:
                if sps not in Concatenation:
                    Concatenation[sps] = ""
                if sps == "CRYPA":
                    print(f)
print(Concatenation)
subdirs , dirs, filenames = next(os.walk(MyDir))
for sd in dirs:
    _, _, filenames = next(os.walk(MyDir+"/"+sd))
    #Repeat the loop:
    for f in filenames:
        if "clean.fasta" in f:
            f_seqs = get_sequence(MyDir+"/"+sd+"/"+f)
            print(isLength(f_seqs))
            for sps in f_seqs:
                Concatenation[sps] += f_seqs[sps]
            currlen = len(f_seqs[sps])
            for sps in Concatenation:
                if sps not in f_seqs:
                    Concatenation[sps] += currlen*"-"
#Generate concatenated file
new_file = open(MyDir+"/Concatenation.fasta", "w")
for sps in Concatenation:
        new_file.write(">"+sps+"\n")
        seq = Concatenation[sps]
        new_file.write(seq+"\n")      


# In[88]:


#Check that the lengths match for each species
for Concatenation in Concatenations:
    print(Concatenation)
    for c in Concatenations[Concatenation]:
        print(c, "-->", len(Concatenations[Concatenation][c]))
    print(len(Concatenation))


# In[39]:


for s in f_seqs:
    print(len(f_seqs[s]))


# In[22]:


gffDir = current + "/gff/"
gffs = {}
subdirs , dirs, filenames = next(os.walk(gffDir)) 
for file in filenames:
    with open(gffDir+file) as f:
        for line in f:
            line = line.split()
            gffs[line[0]] = line[-1]
#Generate concatenated file
new_file = open(gffDir+"/AllGffStrand", "w")
for g in gffs:
    new_file.write(g + "  "+gffs[g]+"\n")

            


# In[ ]:


with open(file) as f:
    for line in f:
        line = line.strip
        uwu[line[0]] = uwu[line[-1]]
return uwu

