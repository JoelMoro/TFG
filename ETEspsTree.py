"""
Program: ETEspsTree.py
Description: Retrieves two species tree. One highliting missng clusters and the other one vanilla and aligned
to fill with colored clades.
"""

from ete3 import PhyloTree, TreeStyle, faces, NodeStyle, AttrFace
import os

tax = {}
maindir = "/home/joelmoro/Documents/Third/Trim2"
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

Color = {}
greens = ["APHIN", "NOTSP"]
reds = ['RETFI', 'ACACA', 'GRENI', 'CRYPR', 'CRYTY', 'CRYUB', 'STRCU', 'CRYAN', 'SPHAR', 'PORUM', 'NANGA', 'GALSU', 'PERSB', 'HALGR', 'CRYMU', 'SYMMI', 'CAPOW', 'CHRSP', 'FONAL', 'HONFE', 'PERSP', 'CRYHO', 'THETR', 'CRYME', 'EMIHU', 'KIPBI', 'SPISA', 'VITBR', 'PLABR', 'PARTE']
print(len(tax))
for c in tax:
    if c in reds:
        Color[c] = "#ff0000"
    elif c in greens:    
        Color[c] = "#008000"
    else:
        Color[c] = "#D9DAD8"

def CustomLayout2(node):
    if node.is_leaf():
        #nameFace = faces.AttrFace("name", fsize=10,)
        #faces.add_face_to_node(nameFace, node, column=0)
        longNameFace = faces.TextFace(tax[node.name])
        faces.add_face_to_node(longNameFace, node, column=0, position = "aligned")

def CustomLayout(node):
    if node.is_leaf():
        nameFace = faces.AttrFace("name", fsize=10, fgcolor=Color[node.name])
        #faces.add_face_to_node(nameFace, node, column=0)
        longNameFace = faces.TextFace(tax[node.name], fgcolor=Color[node.name])
        faces.add_face_to_node(longNameFace, node, column=0)
        nstyle = NodeStyle()
        nstyle["size"] = 0
        nstyle["vt_line_width"] = 4
        nstyle["hz_line_width"] = 4
        nstyle["vt_line_type"] = 0 # 0 solid, 1 dashed, 2 dotted
        nstyle["hz_line_type"] = 0
        nstyle["vt_line_color"] = Color[node.name]
        nstyle["hz_line_color"] = Color[node.name]
        node.set_style(nstyle)



sp100 = PhyloTree(maindir + "/ConcatenationSp100.fasta.treefile")

ts = TreeStyle()
ts.layout_fn = CustomLayout
ts.mode = "c"
sp100.show(tree_style = ts)

ts2 = TreeStyle()
ts2.mode = "c"
ts2.layout_fn = CustomLayout2
ts2.show_leaf_name = False

sp100.show(tree_style = ts2)