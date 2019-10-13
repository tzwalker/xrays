import PackageDeal_XBIC_Fluo_Meta_function as PDeal
import fabio # for opening edf files
import numpy as np #for writing arrays
import math #for using square root
import csv #for writing the csv and reading them
import matplotlib as mpl
import matplotlib.pyplot as plt #for plotting the stuff
import os	#for working with paths 
import re	#for using regular expressions
import glob #for opening all files in a directory
import sys	#for getting Arguments when starting the script


"""
To get this running, you need a folder with the python script PackageDeal_XBIC_Fluo_Meta_function.py and a __init__.py in the same folder as this script.
The input File, here called Wrapping_input.txt, should have the format:
SampleName ScanNumber
SampleName ScanNumber
SampleName ScanNumber
SampleName ScanNumber
...

Where SampleName is here for e.g. CdTe_X_TS58A or CdTe_X_NBL31
The ScanNumber is just the Number e.g. 1 of the scan you want to run
List all scans you want to run in this way.

You need to have the align.spec file in the folder you are running the program. (This lists all the scans of the beamtime, we are getting our metadata from there)

You may have to adapt the paths to the folders where the data is stored, as well as where it shall be saved. This is hardcoded in the PackageDeal_XBIC_Fluo_Meta_function.py.

This program is only compatible with python2.7 the way it is written now.
"""


with open('Wrapping_input.txt') as p:
	for line in p:
		input=line.split(' ')
		PDeal.wrapping(input[0],input[1])
		#print input[1]