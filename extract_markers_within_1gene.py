#!/usr/bin/python
import sys
import os
import fnmatch
from transpose import transpose_fun

# input:
"""
test:
scaf26_sca_1	2	50	51
scaf36_sca_2	2	41	42
test1:
scaf26_50	1	1	2	2
scaf26_50	1	2	1	1
scaf26_51	1	2	1	1
scaf26_51	1	1	1	1
scaf36_41	2	2	2	2
scaf36_41	1	1	1	1
scaf36_42	1	1	1	1
scaf36_42	1	1	1	1
"""

# run:
# ./extract_markers_within_1gene.py test test1
# Comment: superscaffold36 contains both PAR and non-PAR region. Correct the ouput manually.
PAR = ['superscaffold26', 'superscaffold54', 'superscaffold35', 'superscaffold36']
non_PAR= ['superscaffold62', 'superscaffold67', 'superscaffold69-1',
		'superscaffold83', 'superscaffold88', 'superscaffold93', 'superscaffold92',
		'superscaffold63']

infile1 = open(sys.argv[1], "r")
infile2 = open(sys.argv[2], "r")

d1 = {}
for line in infile1:
	line = line.strip("\n").split("\t")
	key = line[0].split("_")[1]+"_"+line[0].split("_")[2]
	value = [line[0].split("_")[0], line[2:]]
	if key in d1:
		d1[key].append(value)
	else:
		d1[key] = value
		
#print d1

for key in d1.keys():
	gene = d1[key][0]
	l = []
	for element in d1[key][1]:
		element = gene+"_"+element
		l.append(element)
	d1[key] = l

#print d1

d2 = {}
for line in infile2:
	line = line.strip("\n").split("\t")
	key = line[0]
	value = line[1:]
	if key in d2:
		d2[key].append(value)
	else:
		d2[key]	= [value]	
#print d2

snps = []
for gene in d1.keys():
	s = []
	for snp in d1[gene]:
		if snp in d2.keys() and snp.split("_")[0] in PAR:
			outfile1 = open(gene+".PAR", "w")
			for l in d2[snp]:
				s.append([snp, l])
	if len(s) > 2: # Check if there is more than one SNP in a gene, len(s) > 2 because there are two lines for each snp
		for element in s:
			snps.append(element[0])
			outfile1.write(element[0]+"\t"+"\t".join(i for i in element[1])+"\n")
	#else: # if just one SNP, remove the file with the gene name
	#	os.remove(gene+"_PAR") 
	outfile1.close()
	
for gene in d1.keys():
	s = []
	for snp in d1[gene]:
		if snp in d2.keys() and snp.split("_")[0] in non_PAR:
			outfile1 = open(gene, "w")
			for l in d2[snp]:
				s.append([snp, l])
	if len(s) > 2: # Check if there is more than one SNP in a gene, len(s) > 2 because there are two lines for each snp
		for element in s:
			snps.append(element[0])
			outfile1.write(element[0]+"\t"+"\t".join(i for i in element[1])+"\n")
	#else: # if just one SNP, remove the file with the gene name
	#	os.remove(gene) 
	outfile1.close()

snps_uniq = set(snps)
for snp in snps_uniq: 
	print snp
			
infile1.close()
infile2.close()


		
