"""
Program: fatigoToRevigoInput.py
Description: Converts the outputs from fatiGO to inputs for reviGO.
"""

import os

results_path = "/home/joelmoro/MN/jmoro/protists/FatiGo_Jaime/results/"

for fn in os.listdir(results_path):
    if "fatigo" in fn:
        name = fn[7:-12]
        terms = {}
        print(name)
        with open(results_path+fn) as f:
            for line in f:
                line = line.strip().split()
                if name == "HGT_results":
                    print(line)
                if "GO:" in line[1] and line[0] != "2":
                    term = line[1]
                    pvalue = line[3]
                    terms[term] = pvalue


    of = open("/home/joelmoro/MN/jmoro/protists/FatiGo_Jaime/results/revigo/revigo_input_"+name+".txt", "w")
    for term in terms:
        print(term+"\t"+terms[term],file=of)
    of.close()

