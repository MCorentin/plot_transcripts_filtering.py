# Plot transcripts filtering

Python script to plot the number of transcript left after filtering a RSEM count matrix. Will also output the information as a tsv file.
A transcript is filtered if its expression is not higher than the threshold in any of the samples.

## Motivation

Useful to assess the level of filtering a transcriptomic assembly will need (lowly expressed transcripts are often artifacts).
However, keep in mind that some relevant transcripts are just lowly expressed.

## Usage

python plot_trancripts_filtering.py -i <i>matrix</i> -r <i>start,stop,step</i> -o <i>outputDir</i>

<i>matrix</i>: RSEM [1] matrix of gene expression (any matrix with samples as columns and transcripts as rows should work, the first line will be considered as a header and will be skipped).

<i>start,stop,step</i>: The filtering range (default: 0, 6, 0.5)

<i>outputDir</i>: The output directory (default current directory)

-n: will skip the plot creation, useful if you have no graphics (you will encounter the "no display available" error).

-v: activate the verbose mode, without this option, the script will be silent (except for errors)

## Output 

For each threshold, the plot prints the number of transcripts left:

![alt text](https://raw.githubusercontent.com/MCorentin/plot_transcripts_filtering.py/master/Nb_transcripts_example.EXPR.matrix.png)


[1] http://deweylab.biostat.wisc.edu/rsem/README.html


## Dependancies

This script uses bash commands to get the number of transcripts at each threshold, so you will need the following executables (all of them are available by default on Linux Systems).
```
    awk
    tail
    wc
```

You will also need the following python packages:
**Note:** The following python packages are already built-in from python2.7 and do not need to be installed:
```
 getopt 
 subprocess 
 sys 
 os 
 shlex
```
- **Python v2 or v3**
- **The following python packages:** [numpy](http://www.numpy.org/ "Numpy Homepage"), [matplotlib.pyplot](https://matplotlib.org/ "Matplotlib Homepage"), getopt, subprocess, sys, os, shlex.
