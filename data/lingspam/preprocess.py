#!/usr/bin/env python3

"""
A script for preprocessing data from the lingspam corpus data set and save it as
a numpy data files. The dataset can be downloaded from
http://www.aueb.gr/users/ion/data/lingspam_public.tar.gz

Usage:

Assuming the data set was downloaded and exctracted to the script's directory
location, you can invoke it as

$ ./preprocess.py lingspam_public/lemm_stop/*/*

This parses all files inside the lemm_stop folder of the data set.

"""
__author__ = "Sérgio Agostinho"
__email__ =  "sergio(dot)r(dot)agostinho(at)gmail.com"


import sys
import re
import os.path
import numpy as np

def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate


# Mimicking the static variable functionality from C
# p1 replace connections
# p2:
# - filter everything with less than 3 chars mid string
# - filter everything with less than 3 chars string start
# - filter everything non alfanumeric end of string
# p3 remove duplicate spaces
# p4 All numbers are treated the same
@static_vars(p1=re.compile(r"-"),\
			 p2=re.compile(r" ([^ ]{1,2} )+|^([^ ]{1,2} )+|[^a-zA-Z0-9]+?$"),\
			 p3=re.compile(r" {2,}"),\
			 p4=re.compile(r"\b[\d]+\b"))
def filter_email(content: str):
	return filter_email.p4.sub("#",\
		filter_email.p3.sub(" ",\
		filter_email.p2.sub(" ",\
		filter_email.p1.sub(" ", content)))).strip()



# Storage Holders
target_names = ["ham", "spam"]
targets = []
file_names = []
words = []

# script accepts path wildcards
pr = re.compile("spmsg")
for i, path in enumerate(sys.argv[1:]):

	# Retrieve and store file name
	file_name = os.path.basename(path)
	file_names.append(file_name)

	# Check if spam
	targets.append(bool(pr.match(file_name)))

	# Store list with email words
	content = str(open(path).read()).splitlines()[2]
	email_words = filter_email(content).split()
	words.append(email_words)

	# Create a counter object from the words
	sys.stdout.write("\r%.1f%%" % (i * 100/ (len(sys.argv) - 1)))
	sys.stdout.flush()

print("\nTargets: ", len(targets), " ", targets[0])
print("FileNames: ", len(file_names), " ", file_names[0])
print("Words: ", len(words), " ", words[0][0:10])

np.savez("lingspam",\
			file_names=np.array(file_names, dtype=str),\
			target_names=np.array(target_names, dtype=str),\
			targets=np.array(targets, dtype=bool),\
			words=np.array(words, dtype=list))
