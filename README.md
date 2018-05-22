# Plot transcripts filtering

Python script to plot the number of transcript left after filtering a RSEM count matrix.
A transcript is filtered if its expression is not higher than the threshold in any of the samples.

## Motivation

Useful to assess the level of filtering a transcriptomic assembly will need (lowly expressed transcripts are often artifacts).

## Usage

python plot_TPM_values.py -i <i>matrix</i> -r <i>start,stop,step</i> -o <i>outputDir</i>

<i>matrix</i>: RSEM [1] matrix of gene expression (any matrix with samples as columns and transcripts as rows should work, the first line will be considered as a header and will be skipped).

<i>start,stop,step</i>: The filtering range (default: 0, 6, 0.5)

<i>outputDir</i>: The output directory (default current directory)

# Output 

For each threshold, the plot prints the number of transcripts left:

![alt text](https://raw.githubusercontent.com/MCorentin/plot_TPM_values.py/master/example.png)



[1] http://deweylab.biostat.wisc.edu/rsem/README.html
