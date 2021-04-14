#!/bin/bash

# Set paths and variables
long_reads= #/path/to/long/reads
short_reads= #/path/to/short/reads
strain=#strain name
min_len=#miniumum read length for nanopore reads
threads=#Number of available threads
genome_size=#Approximate genome size


# Subset short reads to reduce memory requirement and build FM index
head -n 3200000 ${short_reads} | awk 'NR % 4 == 2' | sort | tr TN NT | ropebwt2 -LR | tr TN NT | fmlrc2-convert ${strain}.npy

# Remove long reads that are short to reduce run time
python subset_long_reads.py ${long_reads} ${strain}.long.filtered.fasta $min_len

# Correct long reads
fmlrc2 -t $threads ${strain}.npy ${strain}.long.filtered.fasta ${strain}.long.corrected.fasta

# Assemble corrected reads
flye -g $genome_size --nano-corr ${strain}.long.corrected.fasta -o ${strain}
