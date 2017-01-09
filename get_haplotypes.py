#!/usr/bin/python
import sys
import warnings

""" 
Homa Papoli. 09.01.17
This script counts the number of haplotypes present in the population and recode
the file as a biallelic marker.
Usage: ./get_haplotypes.py input1
"""

# input1 example: Sca_R000806.csv_2
input1 = open(sys.argv[1], "r")
# output name is the input name
output = open(sys.argv[1].split("_")[1], "w")

# Read the haplotypes into a list
hap_list = []
for line in input1:
	line = line.strip("\n").strip(" ")
	if not line.startswith("#"):
		hap_list.append(line)
#print hap_list

# If any haplotype contained zero in hap_list, Raise Exception
# The script should be improved by correcting for missing data, for now, it 
# raises an exception when 
for haplotype in hap_list:
	if '0' in haplotype:
		#raise ValueError("haplotype contains zero")
		warnings.warn("This haplotype set contains missing data")
		print sys.argv[1]
		break
# Get a unique set of haplotypes available
uniq_haps = list(set(hap_list))

print uniq_haps

# Build a dictionary with haplotype as key and the index of the haplotype in the 
# list plus 1 as the allele number
haplo_dict = {}
for index, value in enumerate(uniq_haps):
	if '9' in value:
		haplo_dict[value] = "W_linked"
	else:
		haplo_dict[value] = index+1

print sys.argv[1].split("_")[1], haplo_dict

# Replace each genotype with the new code indicated in haplo_dict
new_hap = []
for element in hap_list:
	new_hap.append(haplo_dict[element])
	
#print new_hap
		
# Read haplotypes as pairs which represent the genotype of an individual 
hap_geno = zip(new_hap[::2], new_hap[1::2])

# write each genotype in the output
for element in hap_geno:
	output.write(str(element[0])+" "+str(element[1])+"\n")

