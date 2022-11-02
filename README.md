These scripts are used to evaluate sgRNA library that the number of reads that don't match U6 transcript pattern, that match U6 transcript pattern but NOT in design library (non-perfect match) and that match U6 transcript pattern and IN design library (perfect match).

# Usage

```bash
python sgRNA_library_calculator.py -f fastq-1.gz,fastq-2.gz -l design_library -r reference -o output

    -h get this help and exit.
    -f fastq files, comma seperate.
    -l designed sgRNA library, at least two columns, without header, of gene IDs and sgRNA sequences without PAM.
    -r amplicon reference, fasta format.
    -g guide spacer for mouse library, provide with CGAAACACCG (default). For human library, should provide with CGAAACACC.
    -o output file name.
    -t number of threads.
    -q quality phred value, default is 30.
    -v print version (sgRNA_library_calculator.py v0.3) and exit.
```

# Requirements

- Python3
- fastp
- bowtie2
- FLASH

# Contact

If you encounter any problems or have any questions, please feel free to create an issue at (github issue)[https://github.com/fuhuancheng/sgRNA_library_calculator/issues] or send me an email.

