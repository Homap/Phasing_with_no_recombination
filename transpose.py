#!/usr/bin/python
import sys


def transpose_fun(f):
	"""transpose is a function that takes a matrix, f, 
	transposes it and returns a list. To print the 
	matrix, one should iterate over the elements in the
	list."""
	content = f.readlines()
	content = [x.strip().split("\t") for x in content]
	tr_content = [list(i) for i in zip(*content)]
	return tr_content



