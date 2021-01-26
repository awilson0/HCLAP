# Bacterial Genome Assembly pipeline
This pipeline can be used to automatically assemble bacterial genomes using a fast, accurate hybrid approach.

## Installation
You will need several tools installed to run this pipeline.

* Nextflow: Available on Cedar with the command `module load nextflow`
* Rust: Available on Cedar with the command `module load rust`
* Flye: Available through conda
* ropebwt2: Available through conda
* FMLRC2: With Rust loaded, run `cargo install fmlrc`

## Required data
This pipeline requires two input files per genome: one file containing long reads and one containing short reads. If the short read library was paired-end, you can contatenate the two files with `cat strain_1.fastq strain_2.fastq > strain_short.fastq`. The minimum long read coverage to get a complete assembly is about 20x coverage but it will vary depending on median read length. The minimum short read coverage hasn't been determined yet, but I've managed to get high quality assemblies with 20x coverage.
