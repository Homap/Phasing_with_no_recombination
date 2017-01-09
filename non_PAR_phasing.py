#!/usr/bin/python
import sys
import collections

"""
Homa Papoli - 09.01.17
non_PAR_phasing.py takes a set of markers in the non-pseudoautosomal section 
of the Z chromosome for which r=0 in males and determines the haplotype based
on the following logic:
mothers have one haplotype
one of sons' haplotype is that of the mother
daughter's haplotype is one of the fathers
Pedigree contains two generations. 
input1 has the following format:
familyID\tindID\tfather\tmother\tsex\tstatus\tallele1 allele2 allele3 allele4
the second allele in females have been coded with "9"

Run the script as follows ./non_PAR_phasing.py input1 > output
"""

input1 = open(sys.argv[1], "r")

# Read parents genotypes into the parents dictionary
parents_unord = {}
offspring_unord = {}
for line in input1:
	line = line.strip("\n").split("\t")
	family = int(line[0])
	if line[2] == '0':
		if family in parents_unord:
			parents_unord[family].append(line[6])
		else:
			parents_unord[family] = [line[6]]
# Read offspring genotypes into the offspring dictionary
	if line[2] != '0':
		if family in offspring_unord:
			offspring_unord[family].append(line[6])
		else:
			offspring_unord[family] = [line[6]]	

parents = collections.OrderedDict(sorted(parents_unord.items()))
offspring = collections.OrderedDict(sorted(offspring_unord.items()))


# Start finding the haplotypes. Store haplotypes in the following dictionaries:
parents_haplotypes = {}
offspring_haplotypes = {}
for key in parents:
	father=[]
	mother=[]
# Take mother's haplotype
	mother_gen = parents[key][1]
	hap_geno_m = zip(mother_gen.split(' ')[::2], mother_gen.split(' ')[1::2])
	mother_hap = [genotype[0] for genotype in hap_geno_m]
	mother.append(" ".join(i for i in mother_hap))
	mother.append(" ".join(i for i in ['9' for i in mother_hap]))
	if key in parents_haplotypes.keys():
		print "Error"
		break
	else:
		parents_haplotypes[key] = [mother]
# The offspring dictionary is sorted so the order of offspring is kept accordingly.
	for gen in offspring[key]:
		t = []
# Take daughter's haplotype
		if '9' in gen:
			hap_geno = zip(gen.split(' ')[::2], gen.split(' ')[1::2])
			daughter_hap = [genotype[0] for genotype in hap_geno]
			t.append(" ".join(i for i in daughter_hap))
			t.append(" ".join(i for i in ['9' for i in daughter_hap]))
			if key in offspring_haplotypes.keys():
				offspring_haplotypes[key].append(t)
			else:
				offspring_haplotypes[key] = [t]	
		else:
# Take son's haplotype
			hap_geno = zip(gen.split(' ')[::2], gen.split(' ')[1::2])
			son_hap_1 = mother_hap
			son_hap_2 = []
			for index, value in enumerate(son_hap_1):
				if value == hap_geno[index][0] and value == hap_geno[index][1]:
					son_hap_2.append(hap_geno[index][0])
				else:
					son_hap_2.append(list(set(hap_geno[index]) - set([value]))[0])
					
			t.append(" ".join(i for i in son_hap_1))
			t.append(" ".join(i for i in son_hap_2))
			if key in offspring_haplotypes.keys():
				offspring_haplotypes[key].append(t)
			else:
				offspring_haplotypes[key] = [t]

# Take father's haplotype
	father_gen = parents[key][0]
	hap_geno_f = zip(father_gen.split(' ')[::2], father_gen.split(' ')[1::2])
	father_hap_1 = son_hap_2

	father_hap_2 = []
	for index, value in enumerate(father_hap_1):
		if value == hap_geno_f[index][0] and value == hap_geno_f[index][1]:
			father_hap_2.append(hap_geno_f[index][0])
		else:
			father_hap_2.append(list(set(hap_geno_f[index]) - set([value]))[0])
	father.append(" ".join(i for i in father_hap_1))
	father.append(" ".join(i for i in father_hap_2))
	if key in parents_haplotypes.keys():
		parents_haplotypes[key].append(father)
	else:
		parents_haplotypes[key] = [father]
	
# print offspring_haplotypes
# print parents_haplotypes

# Printing the output
count = 0
for key in parents_haplotypes.keys():
	count += 1
	print ("#"+str(key)+"_"+str(count)+"_"+"father")
	print "\n".join(i for i in parents_haplotypes[key][1])
	count +=1 
	print ("#"+str(key)+"_"+str(count)+"_"+"mother")
	print "\n".join(i for i in parents_haplotypes[key][0])
	for index, value in enumerate(offspring_haplotypes[key]):
		count += 1
		print ("#"+str(key)+"_"+str(count)+"_"+"offspring")
		print "\n".join(i for i in value)
	


