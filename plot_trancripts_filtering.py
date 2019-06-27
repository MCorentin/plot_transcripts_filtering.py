#!/usr/bin/python

# Plot the number of transcripts against expression value, use counts matrix as input

import os
import getopt
import sys
import shlex
import numpy as np
from subprocess import call, Popen, PIPE
import matplotlib.pyplot as plt


def usage():
	print("Usage:")
	print("	python plot_transcripts_filtering.py -i [isoforms.matrix] -r [start,stop,step] -o [outDir]\n")
	print("Input:")
	print("	-i / --matrix file containing the counts matrix (isoforms or genes)")
	print("	-r / --range for filtering range (format: start,stop,step) (default:0,6,0.5)")
	print("output:")
	print("	-o / --outputDir for output directory (default: current directory)")
	print("	-n / --noplot to skip the plot generation")
	print("")
	print("-h / --help for help")
	print("-v / --verbose to activate verbose mode")


# Default values
outDir = "./"
matrix = None
start = 0
stop = 6
step = 0.5
verbose = False
noplot = False

################################## GET OPTS ##################################################
try:
    opts, args = getopt.getopt(sys.argv[1:], "hi:r:o:vn", ["help", "matrix=", "range=", "outputDir=", "verbose", "noplot"])
except getopt.GetoptError as err:
	# will print something like "option -a not recognized"
    print(str(err))
	# print help information and exit:
    usage()
    sys.exit(2)

for o, a in opts:
	if o in ("-i", "--matrix"):
		matrix = a
	elif o in ("-r", "--range"):
		start,stop,step = a.split(",")
		start = float(start)
		stop = float(stop)
		step = float(step)
	elif o in ("-o", "--outputDir"):
		outDir = a
	elif o in ("-h", "--help"):
		usage()
		sys.exit()
	elif o in ("-v", "--verbose"):
		verbose = True
	elif o in ("-n", "--noplot"):
		noplot = True
	else:
		assert False, "unhandled option"

# Check Input
if(matrix == None):
	print("Please provide a count matrix as input (option -i / --matrix)\n")
	usage()
	sys.exit()

if(outDir == None):
	print("Please provide output directory (option -o / --outputDir)\n")
	usage()
	sys.exit()

if not(isinstance(start,(int, float))):
	print("Check your range, 'start' is not an int or float !\n")
	sys.exit()

if not(isinstance(stop, (int, float))):
	print("Check your range, 'stop' is not an int or float !\n")
	sys.exit()

if not(isinstance(step, (int, float))):
	print("Check your range, 'step' is not an int or float !\n")
	sys.exit()

if not(os.path.isdir(outDir)):
	print(str(outDir)+" is not a directory !\n")
	sys.exit()

if not(os.path.exists(matrix)):
	print(str(matrix)+" does not exists !\n")
	sys.exit()


################################## PLOT ########################################################
thresholds = list()
nbIsoforms = list()

# We need to create the plot now to add the text as we go along the filtering in the loop below
if(noplot == False):
	plt.figure(figsize=(20,10))

if(verbose == True):
	print(matrix)

#For each TPM thresholds in 'range'
for tpmThreshold in np.arange(start, stop+step, step):
	if(verbose == True):
		print("Current Threshold: " + str(tpmThreshold))

	# First, remove header line from the matrix
	cmd1 = "tail -n +2 " + str(matrix)
	p1 = Popen(shlex.split(cmd1), shell=False, stdout=PIPE)

	# Then keep the line only if max_expressed(Transcript) > current_threshold
	cmd2 = "awk \'{max=$2; for(i=2;i<=NF;i++) if($i>max) max=$i; if(max >= " + str(tpmThreshold) + ") {print max};}\'"
	p2 = Popen(shlex.split(cmd2), shell=False, stdin=p1.stdout, stdout=PIPE)

	# Finally get the number of transcript for the result
	cmd3 = "wc -l"
	result = Popen(shlex.split(cmd3), shell=False, stdin=p2.stdout, stdout=PIPE).communicate()[0]
	# Popen is outputing bytes, so we use "decode()" to change it to string
	result = result.decode()

	# 'thresholds' and 'nbIsoforms' works in parallel: thresholds[i] corresponds to nbIsoforms[i]
	thresholds.append(tpmThreshold)
	nbIsoforms.append(result)

	#Plot coordinates in the plot next to the dots
	strResult = str(result).replace("\n", "")
	
	if(noplot == False):
		plt.text(tpmThreshold, result, "("+strResult+")")

	if(verbose == True):
		print("Number of transcripts: " + strResult + "\n")


# Saving output as txt file
textOutputFile = outDir + "/Nb_transcripts_"+ os.path.basename(matrix)+".txt"

if(verbose == True):
		print("Saving txt output in:" + textOutputFile + "\n")

index = 0
with open(textOutputFile, "w") as outTxtFile:
	outTxtFile.write("Threshold\tNumber_Isoforms_Left\n")
	while index < len(thresholds):
		outTxtFile.write(str(thresholds[index])+"\t"+str(nbIsoforms[index]))
		index = index + 1


# If noplot NOT activated, we plot the figure
if(noplot == False):
	# Print the plot using the lists created in the previous for loop
	plt.scatter(thresholds, nbIsoforms, color='dodgerblue', s=40)
	plt.xlabel('Expression level')
	plt.ylabel('Number of isoforms > expression')
	plt.xlim(start, stop+1)
	plt.title(os.path.basename(matrix))
 
	# Saving graph
	graphFile = outDir + "/Nb_transcripts_"+ os.path.basename(matrix)+".png"
	if(verbose == True):
		print("Saving graph :" + graphFile + "\n")
	plt.savefig(graphFile, bbox_inches='tight')
