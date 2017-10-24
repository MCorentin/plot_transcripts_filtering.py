# Plot TPM Values

Python script to plot the number of transcript left after filtering by TPM (Transcripts Per Million) from a RSEM count matrix.

## Motivation

Useful to assess the level of filtering an Rna seq assembly will need (Low TPM transcripts are often artifacts).

## Usage

python plot_TPM_values.py -i <i>rsemMatrix</i> -r <i>start,stop,step</i> -o <i>outputDir</i>"


# Output 

For each TPM value the plot prints the number of transcripts left:

![alt text](https://raw.githubusercontent.com/MCorentin/plot_TPM_values.py/master/example.png)
