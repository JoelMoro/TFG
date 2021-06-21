#!/usr/bin/env python
# coding: utf-8

"""
Program: VisualizaConcatenateTrees.py
Description: Jupyter notebook export that retrieves the visualization for the three 
concatenation species trees.
"""


# In[17]:


from ete3 import PhyloTree, TreeStyle, faces, NodeStyle, AttrFace
import os


# In[ ]:





# In[2]:


tax = {}
maindir = os.getcwd()
for line in open(maindir + "/taxonomy.txt"):
    line = line.strip()
    dades = line.split("\t")
    if dades[5] == "Pezizomycotina":
        if dades[1] == "BOTFU":
            tax[dades[1]] = dades[9]
        else:
            tax[dades[1]] = dades[6]
    else:
        tax[dades[1]] = dades[2]


# In[12]:


Color = {}
reds = ["APHIN", "NOTSP"]
#oranges = ["ENTDI", "PLACH", "EIMAC", "EIMPR"]
#reds = ["ACACA", "PHYPA", "BODSA", "PLAYO", "PLABE"]
for c in tax:
    if c in oranges:
        Color[c] = "#ffa500"
    elif c in reds:
        Color[c] = "#ff0000"
    else:    
        Color[c] = "#008000"


# In[4]:


sp80 = PhyloTree("ConcatenationSp80.fasta.treefile")


# In[14]:


def CustomLayout(node):
    if node.is_leaf():
        nameFace = faces.AttrFace("name", fsize=10, fgcolor=Color[node.name])
        faces.add_face_to_node(nameFace, node, column=0)
        longNameFace = faces.TextFace(tax[node.name], fgcolor=Color[node.name])
        faces.add_face_to_node(longNameFace, node, column=1, aligned = True)
        nstyle = NodeStyle()
        nstyle["size"] = 0
        nstyle["vt_line_width"] = 4
        nstyle["hz_line_width"] = 4
        nstyle["vt_line_type"] = 0 # 0 solid, 1 dashed, 2 dotted
        nstyle["hz_line_type"] = 0
        nstyle["vt_line_color"] = Color[node.name]
        nstyle["hz_line_color"] = Color[node.name]
        node.set_style(nstyle)


# In[15]:


ts = TreeStyle()
ts.layout_fn = CustomLayout
sp80.show(tree_style = ts)


# In[8]:


#sp125 = PhyloTree("ConcatenationSp125.fasta.treefile")
sp100 = PhyloTree("ConcatenationSp100.fasta.treefile")


# In[16]:


ts = TreeStyle()
ts.mode = "c"
sp100.show(tree_style = ts)


# In[ ]:




