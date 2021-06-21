#First approach to first part of the project


import sys
import re
import random


Cluster = {}
"""
#Dictionary with the following keys and values:
    - First key refers to cluster with value dict
    - Second level keys inside the inner dict refer to species which will also have value dict
    - Third level keys are each individual position with value color.
"""


annots = {} #Will contain the protein family numbers

def int_to_color(seed):

    """
    Given an integer that will act as seed generated a random color
    """
    random.seed(seed)
    r = random.randint(0,255)
    g = random.randint(0,255)
    b = random.randint(0,255)
    return '#%02x%02x%02x' % (r,g,b)

def fix_table(sps):
    """
    Noticed that some species to not match the table name since there are different strains,
    thus, this function adapts the string to be used to the corresponding table
    """

    for i in range(len(sps)):
        if sps[i] == "_":
            sps = sps[:i]
            break
    return sps

def get_color(pos, sps):

    """
    Given the species opens the corresponding table and searches homolog identification
    recognizing the positions of each species as parameter within the cluster and looks for possible color
    """
    if "_" in sps:
        sps_fix = fix_table(sps)
    else:
        sps_fix = sps
    table = "table_"+sps_fix+".txt"
    with open(table) as f:
        for line in f:
            line = re.split('\t', line)
            if line[0] == pos:
                seed = line[1]
                color = int_to_color(seed)
    return color, seed

def read_file(file):

    """
    Reads the main file containing the clusters and creates and fills
    the three-level dictionary.
    """
    print("Reading File....")
    with open(file) as f:
        p_key = ""
        for line in f:
            line = re.split(';|\t|\n| ', line)
            if line[0] == "#":
                p_key = line[1]
                print("Reading", p_key)
                Cluster[p_key] = {}
            else:
                sps = line[0]
                if sps not in Cluster[p_key]:
                    Cluster[p_key][sps] = {}
                for pos in line[1:-1]:
                    color, annot = get_color(pos, sps)
                    Cluster[p_key][sps][pos] = color
                    annots[pos] = annot

def delete_reps(cl):
    """
    Checks for clusters that only have one species which we dont want
    to plot the tree. Also deletes repetitions for clusters with more 
    than one species.
    """
    change_list = []
    c = 0
    for sps in cl:
        base = sps[:-4]
        if base in sps and "_" in sps:
            c += 1
    if c == len(cl):
        print("why")
        return False
    else:
        for sps in cl:
            if "_" in sps:
                sps2 = sps[:-4]
                change_list.append((sps, sps2))
        for duo in change_list:
            cl[duo[1]] = cl.pop(duo[0])
        return True
               
def get_tree(cluster_id):
    """
    Given the cluster id looks in the tree file the newick
    format related to that cluster
    """
    newick = ""
    with open("species_trees_for_clusters.txt") as f:
        for line in f:
            line = line = re.split('\t|\n', line)
            if line[0] == cluster_id:
                newick += line[1]
    return newick

def count_family(cluster):
    """
    Returns a dictioanry with the number of times a protein family appears in a 
    given set of clusters
    """
    Count = {}
    for sps in cluster:
        visited = [] 
        for pos in cluster[sps]:    
            if cluster[sps][pos] not in Count and cluster[sps][pos] not in visited:
                Count[cluster[sps][pos]] = 1
                visited.append(cluster[sps][pos])
            elif cluster[sps][pos] in Count and cluster[sps][pos] not in visited:
                Count[cluster[sps][pos]] += 1
                visited.append(cluster[sps][pos])

    #If only appears once, color it white
    for sps in cluster:
        for pos in cluster[sps]:
            if Count[cluster[sps][pos]] == 1:
                cluster[sps][pos] = "#ffffff"
    return Count

def find_anchor(counter):
    """
    Given the frequency of appearance of each family
    decides the anchor for the plot as the highest freq one.
    """
    possibleAnchors = {}
    for fam in counter:
        possibleAnchors[fam] = True
    anchors = sorted(possibleAnchors,key=lambda x: counter[x])
    anchors.reverse()
    return anchors[0]

def put_cluster_to_matrix(clust, matrix,anchorPos,limits,streamPos, spe, anchor, clust_list):
    """
    Adds a given cluster to the current matrix
    """
    start = limits - anchorPos
    stop = start+len(clust)
    stream = "up"
    
    for i in range(start,stop):
        p = i - start
		#add to matrix
        matrix[spe][i] = clust_list[p]
		#add genes to up or downStream positions
        gene = clust_list[p]
        if clust[gene] == anchor:
            stream = "down"
        if gene != None:
            if clust[gene] not in streamPos[stream]:
                streamPos[stream][clust[gene]] = 0
            streamPos[stream][clust[gene]] += 1

    return matrix, streamPos

def build_matrix(cluster, anchor):
    """
    Given a cluster and its anchor organizes the 
    most fitting distribution according to gene order
    determination
    """
    limits = 0
    first_cluster = ""
    first_spe = ""
    
    for sps in cluster:
        template = []
        for pos in cluster[sps]:
            template.append(pos)
            if anchor == cluster[sps][pos]:
            #find where is anchor and number of regions surrounding
                template.index(pos)
                p = template.index(pos)
                po = len(cluster[sps]) - p
                if p > limits:
                    limits = p
                    first_cluster = cluster[sps]
                    first_spe = sps
                if po > limits:
                    limits = po
                    first_cluster = cluster[sps]
                    first_spe = sps
    #create empty matrix
    matrix = {}
    matrix_limit = limits*10+2
    for sps in cluster:
        matrix[sps] = []
        for i in range(0,matrix_limit):
            matrix[sps].append(0)
    
    #get position for anchor within the cluster
    first_cluster_list = list(first_cluster.keys())
    streamPos = {"up":{},"down":{}}
    anchorPos = locate_anchor(first_cluster, first_cluster_list, anchor)
    matrix, streamPos = put_cluster_to_matrix(first_cluster, matrix, anchorPos, limits, streamPos, first_spe, anchor, first_cluster_list)
    situated = [first_spe]
    for sps in matrix:
        if sps not in situated:
            clust = cluster[sps]
            clust_list = list(clust.keys())
            anchorPos = locate_anchor(clust, clust_list, anchor)
            if anchorPos != None:
                turn = decide_direction(clust, clust_list, anchor, streamPos, sps, anchorPos)
                if turn:
                    clust_list.reverse()
                    anchorPos = locate_anchor(clust, clust_list, anchor)
                matrix, streamPos = put_cluster_to_matrix(clust,matrix,anchorPos,limits,streamPos, sps, anchor, clust_list)
                situated.append(sps)

    #Distribute the reaminging clusters which do not have the anchor
    for sps in matrix:
        if sps not in situated:
            clust = cluster[sps]
            clust_list = list(clust.keys())
            pos1, eval1 = calculate_best_position(streamPos, cluster, clust_list, matrix, first_spe)
            clust_list.reverse()
            pos2, eval2 = calculate_best_position(streamPos, cluster, clust_list, matrix, first_spe)
            
            if eval1 > eval2:
                clust_list.reverse()
                start = pos1
                stop = pos1+len(clust)
            else:
                start = pos2
                stop = pos2+len(clust)
            for i in range(start, stop):
                g = i - start
                matrix[sps][i] = clust_list[g]
    return matrix

def decide_direction(clust, clust_list, anchor, streamPos, sps, anchorPos):
    """
    Decides if the cluster needs to be turned in order to fit the 
    plot under anchor and initial cluster constrains
    """
    tag = "up"
    otag = "down"
    supp1 = 0
    supp2 = 0
    for i in range(0, len(clust)):
        gene = clust_list[i]
        if clust[gene] == anchor:
            tag = "down"
            otag = "up"
        else:
            if clust[gene] in streamPos[tag]:
                supp1 += streamPos[tag][clust[gene]]
            if clust[gene] in streamPos[otag]:
                supp2 += streamPos[otag][clust[gene]]
                
    if supp1 > supp2:
        turn = False
    else:
        turn = True

    return turn

def locate_anchor(clust, clust_list, anchor):
    """
    Returns the position of a protein family member 
    """
    i = 0
    anchorPos = None
    for pos in clust_list:
        if clust[pos] == anchor:
            anchorPos = i
        else:
            i += 1
    return anchorPos

def calculate_best_position(streamPos, cluster, clust_list, matrix, refSps):
    """
    Generates a summary matrix which shows the number
    of times a given gene is present in each column
    """
    summary = {}
    for i in range(0, len(matrix[refSps])):
        counter = {}
        for sps in matrix:
            if matrix[sps][i] != 0:
                gene = matrix[sps][i]
                if cluster[sps][gene] != None:
                    if cluster[sps][gene] not in counter:
                        counter[cluster[sps][gene]] = 0
                    counter[cluster[sps][gene]] += 1
        summary[i] = counter
    old_eval = 0
    chosen = 0
    for i in range(0, len(matrix[refSps])):
        evaluation = 0
        stop = i + len(clust_list)
        if stop <= len(matrix[refSps]):
            for j in range(0, len(clust_list)):
                gene = clust_list[j]
                pos = i + j
                if gene in summary[pos]:
                    evaluation += summary[pos][cluster[refSps][gene]]
            if evaluation > old_eval:
                old_eval = evaluation
                chosen = i

    return chosen, old_eval

def generate_data_for_genoplotR(cluster, cluster_id, annots, matrix, tree_bool):

    """
    Based on the three level dictionary aims to create the dataframes for the
    R file. Pretty much based on Marina's approach for another project.
    """
    
    if tree_bool:
        my_species = []
        for sps in matrix:
            if sps not in my_species:
                my_species.append(sps)    
        #Set up the tree
        newick = get_tree(cluster_id)
        #To do permutation we need to follow newick order
        ordered_species = []
        species_beta = re.findall(r'\w+', newick)
        for sp in species_beta:
            if sp in my_species and sp not in ordered_species:
                ordered_species.append(sp)
    else:
        ordered_species = list(matrix.keys())
     

    #Start Generating the R files
    of = open("GO_"+cluster_id+".R","w")
    print('library(genoPlotR)',file = of)
    dnaList = []
    for sps in ordered_species:
        sps_gff = sps
        sps_gff = fix_table(sps_gff)
        gff_file = sps_gff+".gff"

        names = [""]
        start = ["0"]
        end = ["0"]
        cols = ["#ffffff"]
        strand = ["1"]
        prot_num = ["0"]
        checked = []
        for pos in matrix[sps]:
            if pos != 0:
                #read gff file to decide direction
                with open(gff_file) as f:
                    for line in f:
                        line = line = re.split(';|\t|\n| ', line)
                        if line[-2] == pos and pos not in checked:
                            if line[6] == "+":
                                strand.append("1")  
                            else:
                                strand.append("-1")
                            checked.append(pos)

                names.append(pos)
                cols.append(cluster[sps][pos])       
                prot_num.append(annots[pos])
                index = list(matrix[sps]).index(pos)
                start.append(str(index*5+1))
                end.append(str((index+1)*5))
        line = 'df'+sps+' <- data.frame(name=c("'+'","'.join(names)+'"), '
        line += 'start=c('+','.join(start)+'), '
        line += 'end=c('+','.join(end)+'), '
        line += 'strand=c('+','.join(strand)+'), '
        line += 'col=rep("black"), '
        line += 'fill=c("'+'","'.join(cols)+'"),'
        line += 'gene_type = "arrows",'
        line += 'prot_num = c("'+'","'.join(prot_num)+'"))'
        print(line, file = of)  
        print("dna_seg"+ sps +" <- dna_seg(df"+sps+")",file = of)       
        dnaList.append("dna_seg"+sps)

    if tree_bool:
        print('tree <- newick2phylog('+'"'+newick+'"'+")", file = of)
    print("dna.segs.list <- list("+",".join(dnaList)+")",file=of)
    print('names(dna.segs.list) <- c("'+'","'.join(ordered_species)+'")',file=of)

    #Annotation line requires species and specific positions
    print('annots <- lapply(dna.segs.list, function(x){',file=of)
    print('mid <- middle(x)',file=of)
    print('annot <- annotation(x1=mid,text=x$prot_num,rot=18)',file=of)
    print("})", file = of)

    if tree_bool:
        print("plot_gene_map(dna_segs=dna.segs.list, tree = tree, tree_width = 3, annotations = annots) ", file=of)
    else:
        print("plot_gene_map(dna_segs=dna.segs.list, annotations = annots) ", file=of)


    of.close()



########---------##########
#       Main Code       ###
########---------##########

clust_file = "cluster1.txt"
read_file(clust_file)
for cluster in Cluster:
    print("Running cluster:", cluster, ". . .")
    tree_bool = delete_reps(Cluster[cluster])
    counter = count_family(Cluster[cluster])
    anchor = find_anchor(counter)
    matrix = build_matrix(Cluster[cluster], anchor)
    generate_data_for_genoplotR(Cluster[cluster], cluster, annots, matrix, tree_bool)
    print("Successfully Finished cluster:", cluster, "!")

    
    





