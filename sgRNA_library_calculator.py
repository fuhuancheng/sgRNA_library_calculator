import getopt
import sys, os, datetime

script_path = os.path.split(sys.argv[0])

# version
version = '%s v0.3' %(script_path[1])

# help
help_str = '''
This script will calculate the number of reads that don't match U6 transcript pattern, that match U6 transcript pattern but NOT in design library (non-perfect match) and that match U6 transcript pattern and IN design library (perfect match).

Usage:

python %s -f fastq-1.gz,fastq-2.gz -l design_library -r reference -o output

    -h get this help and exit.
    -f fastq files, comma seperate.
    -l designed sgRNA library, at least two columns, without header, of gene IDs and sgRNA sequences without PAM.
    -r amplicon reference, fasta format.
    -g guide spacer for mouse library, provide with CGAAACACCG (default). For human library, should provide with CGAAACACC.
    -o output file name.
    -t number of threads.
    -q quality phred value, default is 30.
    -v print version (%s) and exit.

''' %(script_path[1], version)

# default values
# default mouse library;
key_g = "CGAAACACCG"
# default output name
output = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
# default threads
threads = 1
# default phred value 30
phred = '30'
# default unqualified percent
unqualified_percent = '40'

opts, args = getopt.getopt(sys.argv[1:], "-h-g:-l:-f:-r:-o:-t:-v-q:")

# print version, help
for opt_name, opt_value in opts:
    if opt_name in ('-v'):
        print(version)
        sys.exit()
    elif opt_name in ("-h"):
        print(help_str)
        sys.exit()

# if no fastq or reference, print help and exit
try:
    for opt_name, opt_value in opts:
        if opt_name in ("-f"):
            fastq = opt_value
        elif opt_name in ("-r"):
            reference = opt_value
    if fastq == '' or reference == '':
        sys.exit()
except:
    print(help_str)
    sys.exit()

# library, guide key, output name, threads
for opt_name, opt_value in opts:
    if opt_name in ("-l"):
        library = opt_value
    elif opt_name in ("-g"):
        key_g = opt_value
    elif opt_name in ("-o"):
        output = opt_value
    elif opt_name in ("-t"):
        threads = opt_value
    elif opt_name in ('-q'):
        phred = opt_value


# split fastq into seperated fastq files
fastqs = fastq.split(',')
fastqs_out = [fastqs[0]+'.filtered', fastqs[1]+'.filtered']

# directory for output

# reference file name
ref_file = os.path.split(reference)[1]

# using fastp for quality filtered
fastp = 'fastp --qualified_quality_phred %s --unqualified_percent_limit %s --in1 %s --out1 %s --in2 %s --out2 %s --thread %s' %(phred, unqualified_percent, fastqs[0], fastqs_out[0], fastqs[1], fastqs_out[1], threads)

# flash command
fastq = ' '.join(fastqs_out)
flash = 'flash --max-overlap=150 -o %s -z -t %s %s' %(output, threads, fastq)

# bowtie2 index
bowtie_build = 'bowtie2-build %s %s' %(reference, ref_file)

# bowtie2 alignment
bowtie = 'bowtie2 -x %s -p %s -U %s.extendedFrags.fastq.gz -S %s.sam' %(ref_file, threads, output, output)

# sgRNA calculate
sgRNA_count_path = os.path.join(script_path[0], 'sgRNA_count.py')
sgRNA_count = 'python %s %s %s.sam > %s.csv' %(sgRNA_count_path, key_g, output, output)

fastp_log = os.popen(fastp).read()
flash_log = os.popen(flash).read()
bowtie_build_log = os.popen(bowtie_build).read()
bowtie_log = os.popen(bowtie).read()
sgRNA_count_log = os.popen(sgRNA_count).read()

with open('%s-%s.log' %(output, script_path[1]), 'w') as log:
    log.write('#'*20+'\n')
    log.write('fastp QC log.\n%s\n\n' %(fastp))
    log.write(fastp_log)

    log.write('#'*20+'\n')
    log.write('FLASH merged log.\n%s\n\n' %(flash))
    log.write(flash_log)

    log.write('#'*20+'\n')
    log.write('bowtie2 index build log.\n%s\n\n' %(bowtie_build))
    log.write(bowtie_build_log)

    log.write('#'*20+'\n')
    log.write('bowtie2 mapping log.\n%s\n\n' %(bowtie))
    log.write(bowtie_log)

    log.write('#'*20+'\n')
    log.write('sgRNA counting log.\n%s\n\n' %(sgRNA_count))
    log.write(sgRNA_count_log)
    
    log.write('#'*20+'\n')
    

