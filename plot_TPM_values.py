#!/usr/bin/python

# Plot the number of isoforms against TPM value

import os
import getopt
from subprocess import call, Popen, PIPE
import numpy as np
import matplotlib.pyplot as plt

def usage:
	print "-h for help\nInput:\n	-r for rsem directory\n	-i to take isoforms.results instead of genes.results\noutput:\n	-o for output directory\n"


try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:r:", ["help", "output=", "rsemDir="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    # If geneResult == T => considers genes.results in RSEM, or else isoforms.results
    geneResult = T
    output = None
    rsemDir = None
    for o, a in opts:
        if o in ("-r", "--rsemDir"):
            rsemDir = a
        elif o in ("-o", "--output"):
            output = a
	elif o in ("-h", "--help"):
            usage()
            sys.exit()
        else:
            assert False, "unhandled option"



if(rsemDir == None):
	print "Please provide rsem directory as input (option -r / --rsemDir)"
	sys.exit()

if(output == None)
	print "Please provide output directory (option -o / --output)"
        sys.exit()


cmd = "find " + rsemDir + " -name '*.isoforms.results'"
samples = Popen(cmd, shell=True, stdout=PIPE).communicate()[0].split("\n")

for s in samples:
	if s != "":
		thresholds = list()
		nbIsoforms = list()
		###### PLOT #####
		plt.figure(figsize=(20,10))
		print(s)
		#For each TPM threshld
		for tpmThreshold in range(0,6):
			cmd = "cat " + s + " | awk '$6 >= "+str(tpmThreshold)+" { print $6 }' | wc -l"

			#Get the number of isoforms with TPM > threshold
			result = Popen(cmd,shell=True,stdout=PIPE).communicate()[0]
			thresholds.append(tpmThreshold)
			nbIsoforms.append(result)

			#Plot coordinates in the plot
			strResult = str(result).replace("\n", "")
			#print(strResult)
			plt.text(tpmThreshold, result, "("+strResult+")")

		#Print the plot
		plt.scatter(thresholds, nbIsoforms, color='dodgerblue', s=40)
		plt.xlabel('TPM')
		plt.ylabel('Number of isoforms > TPM')
		plt.title(os.path.basename(s))

		#plt.show()
		graphDir = rsemDir + "graphs/Nb_isoforms_TPM_"+ os.path.basename(s)
		print "Saving graph into" + graphDir
		plt.savefig(graphDir +".png", bbox_inches='tight')
