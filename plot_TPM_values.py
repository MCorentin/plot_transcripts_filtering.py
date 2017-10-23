#!/usr/bin/python

# Plot the number of transcripts against TPM value

import os
import getopt
import sys
import numpy as np
from subprocess import call, Popen, PIPE
import matplotlib.pyplot as plt


def usage():
	print "-h / --help for help\nInput:\n	-i / --rsemMatrix file containing the TPM counts matrix (isoforms or genes)\n	-r / --range for filtering range (format: start,stop,step) default:0,6,0.5\noutput:\n	-o / --outputDir for output directory\n"


################################## GET OPTS ##################################################
try:
	opts, args = getopt.getopt(sys.argv[1:], "hi:r:o:", ["help", "rsemMatrix=", "range=", "outputDir="])
except getopt.GetoptError as err:
        # print help information and exit:
        print str(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

# If geneResult == T => considers genes.results in RSEM, or else isoforms.results
geneResult = "F"
outDir = None
rsemMatrix = None
start = 0
stop = 6
step = 0.5

for o, a in opts:
	if o in ("-i", "--rsemMatrix"):
		rsemMatrix = a
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
	else:
		assert False, "unhandled option"


if(rsemMatrix == None):
	print "Please provide rsem TPM Matrix as input (option -i / --rsemMatrix)\n"
	print "Usage:\n"
	usage()
	sys.exit()

if(outDir == None):
	print "Please provide output directory (option -o / --outputDir)\n"
        print "Usage:\n"
        usage()
	sys.exit()

# Double check for range
if not(isinstance(start,(int, long, float))):
	print("Check your range, 'start' is not an int, long or float !\n")
        sys.exit()

if not(isinstance(stop, (int, long, float))):
	print("Check your range, 'stop' is not an int, long or float !\n")
        sys.exit()

if not(isinstance(step, (int, long, float))):
	print("Check your range, 'step' is not an int, long or float !\n")
	sys.exit()


################################## PLOT ########################################################

thresholds = list()
nbIsoforms = list()

plt.figure(figsize=(20,10))
print(s)
#For each TPM threshld
for tpmThreshold in np.arange(start, stop, step):
	#Get the number of isoforms with sum(TPM) > threshold
	# "tail -n +2" is to skip the header (samples names)
	# "awk '{for(i=1;i<=NF;i++) t+=$i; if(t>"+threshold+"){print t}; t=0}'" is to print the list of sums for all samples with sum(TPM) > threshold
	# wc -l is to count the lines printed at the previous "step"
	cmd = "tail -n +2 " + rsemMatrix + " | awk '{for(i=1;i<=NF;i++) t+=$i; if(t>"+threshold+"){print t}; t=0}' | wc -l
	
	result = Popen(cmd,shell=True,stdout=PIPE).communicate()[0]
	thresholds.append(tpmThreshold)
	nbIsoforms.append(result)

	#Plot coordinates in the plot
	strResult = str(result).replace("\n", "")
	plt.text(tpmThreshold, result, "("+strResult+")")

	#Print the plot
	plt.scatter(thresholds, nbIsoforms, color='dodgerblue', s=40)
	plt.xlabel('TPM')
	plt.ylabel('Number of isoforms > TPM')
	plt.title(os.path.basename(s))

	#plt.show()
	graphFile = outDir + "/Nb_isoforms_TPM_"+ os.path.basename(s)
	print "Saving graph :" + graphFile + "\n"
	plt.savefig(graphFile +".png", bbox_inches='tight')
