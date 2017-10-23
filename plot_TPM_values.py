#!/usr/bin/python

# TO ADD :
#	-r --range : to consider a range and step for the TPM filtering

# Plot the number of isoforms against TPM value

import os
import getopt
import sys
import numpy as np
from subprocess import call, Popen, PIPE
import matplotlib.pyplot as plt


def usage():
	print "-h / --help for help\nInput:\n	-i / --rsemDir for rsem directory\n	-r / --range for filtering range (format: start,stop,step) default:0,6,0.5\noutput:\n	-o / --outputDir for output directory\n"


################################## GET OPTS ##################################################
try:
	opts, args = getopt.getopt(sys.argv[1:], "hi:r:o:", ["help", "rsemDir=", "range=", "outputDir="])
except getopt.GetoptError as err:
        # print help information and exit:
        print str(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

# If geneResult == T => considers genes.results in RSEM, or else isoforms.results
geneResult = "F"
outDir = None
rsemDir = None
start = 0
stop = 6
step = 0.5

for o, a in opts:
	if o in ("-i", "--rsemDir"):
		rsemDir = a
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


if(rsemDir == None):
	print "Please provide rsem directory as input (option -i / --rsemDir)\n"
	print "Usage:\n"
	usage()
	sys.exit()

if(outDir == None):
	print "Please provide output directory (option -o / --outputDir)\n"
        print "Usage:\n"
        usage()
	sys.exit()


samples = None
cmd = "find " + rsemDir + " -name '*.isoforms.results'"
samples = Popen(cmd, shell=True, stdout=PIPE).communicate()[0].split("\n")
if(samples == None):
	print "Could not find rsem results file in folder\n"
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

for s in samples:
	if s != "":
		thresholds = list()
		nbIsoforms = list()

		plt.figure(figsize=(20,10))
		print(s)
		#For each TPM threshld
		for tpmThreshold in np.arange(start, stop, step):
			# Command to filter the TPM column (the 6th one) bu threshold and count the number of lines
			cmd = "cat " + s + " | awk '$6 >= "+str(tpmThreshold)+" { print $6 }' | wc -l"

			#Get the number of isoforms with TPM > threshold
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
