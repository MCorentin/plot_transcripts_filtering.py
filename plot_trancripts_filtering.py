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
	print "-h / --help for help\nInput:\n	-i / --rsemMatrix file containing the counts matrix (isoforms or genes)\n	-r / --range for filtering range (format: start,stop,step) default:0,6,0.5\noutput:\n	-o / --outputDir for output directory\n"

# Default values
outDir = "./"
rsemMatrix = None
start = 0
stop = 6
step = 0.5


################################## GET OPTS ##################################################
try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:r:o:", ["help", "rsemMatrix=", "range=", "outputDir="])
except getopt.GetoptError as err:
        # print help information and exit:
        print str(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

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

# Check Input
if(rsemMatrix == None):
	print "Please provide RSEM TPM Matrix as input (option -i / --rsemMatrix)\n"
	print "Usage:\n"
	usage()
	sys.exit()

if(outDir == None):
	print "Please provide output directory (option -o / --outputDir)\n"
        print "Usage:\n"
        usage()
	sys.exit()

if not(isinstance(start,(int, long, float))):
	print("Check your range, 'start' is not an int, long or float !\n")
        sys.exit()

if not(isinstance(stop, (int, long, float))):
	print("Check your range, 'stop' is not an int, long or float !\n")
        sys.exit()

if not(isinstance(step, (int, long, float))):
	print("Check your range, 'step' is not an int, long or float !\n")
	sys.exit()

if not(os.path.isdir(outDir)):
	print(str(outDir)+" is not a directory !\n")
        sys.exit()

if not(os.path.exists(rsemMatrix)):
	print(str(rsemMatrix)+" does not exists !\n")
        sys.exit()


################################## PLOT ########################################################
thresholds = list()
nbIsoforms = list()

plt.figure(figsize=(20,10))

print(rsemMatrix)

#For each TPM thresholds in 'range'
for tpmThreshold in np.arange(start, stop+step, step):
	print("Current Threshold: " + str(tpmThreshold))

	#cmd = str('tail -n +2 ') + str(rsemMatrix) + str(" | awk \'{max=$2; for(i=2;i<=NF;i++) if($i>max) max=$i; if(max >= ") + str(tpmThreshold) + str(") {print max};}\' | wc -l")

	# First, remove header line from the matrix
	cmd1 = "tail -n +2 " + str(rsemMatrix)
	p1 = Popen(shlex.split(cmd1), shell=False, stdout=PIPE)

	# Then keep the line only if max_expressed(Transcript) > current_TPM_threshold
	cmd2 = "awk \'{max=$2; for(i=2;i<=NF;i++) if($i>max) max=$i; if(max >= " + str(tpmThreshold) + ") {print max};}\'"
	p2 = Popen(shlex.split(cmd2), shell=False, stdin=p1.stdout, stdout=PIPE)

	# Finally get the number of transcript for the result
	cmd3 = "wc -l"
	result = Popen(shlex.split(cmd3), shell=False, stdin=p2.stdout, stdout=PIPE).communicate()[0]

	# 'thresholds' and 'nbIsoforms' works in parallel: thresholds[i] corresponds to nbIsoforms[i]
	thresholds.append(tpmThreshold)
	nbIsoforms.append(result)

	#Plot coordinates in the plot next to the dots
	strResult = str(result).replace("\n", "")
	plt.text(tpmThreshold, result, "("+strResult+")")

	print("Number of transcripts: " + strResult + "\n")

# Print the plot using the lists created in the previous for loop

plt.scatter(thresholds, nbIsoforms, color='dodgerblue', s=40)
plt.xlabel('Expression level')
plt.ylabel('Number of isoforms > expression')
plt.xlim(start, stop+1)
plt.title(os.path.basename(rsemMatrix))


# Saving graph
graphFile = outDir + "/Nb_transcripts_"+ os.path.basename(rsemMatrix)
print "Saving graph :" + graphFile + "\n"
plt.savefig(graphFile +".png", bbox_inches='tight')
