# Plot TPM Values

Python Script to plot the Number of Transcript left after filtering by TPM (Transcripts Per Million) from a RSEM output

## Motivation

Useful to assess the level of filtering an Rna seq assembly will need (Low TPM transcripts are often artifacts)

## Usage

python plot_TPM_values.py -i <rsemDirectory> -r <start,stop,step> -o <outputDir>

The RSEM directory must contain a *.isoform.results file with the TPM values as the 6th column

# Output 

For each TPM value the plot prints the number of transcripts left:

![alt text](https://raw.githubusercontent.com/MCorentin/plot_TPM_values.py/master/example.png)
