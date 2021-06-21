"""
Program: get_evoldecisions.py
Description: Checks the evolutionary history of each cluster and obtains the non-verticals.
"""

import os

classifier_file = "/home/joelmoro/MN/jmoro/protists/MyEvolclust/results/evolclassifier.results.txt"
not_vertical = {}
with open(classifier_file) as f:
    header = False
    for line in f:
        line = line.strip().split("\t")
        if header and line[-1] != "VE":
            print(line[-1])
            not_vertical[line[0]] = line[-1]
        if not header:
            header = True

of = open("/home/joelmoro/MN/jmoro/protists/MyEvolclust/results/not_verticals.txt", "w")
for id in not_vertical:
    print(id,file=of)
of.close()