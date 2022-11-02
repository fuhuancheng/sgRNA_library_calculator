# usage: python sgRNA_count.py key sam.file

import sys, fileinput, re

# import pysnooper
# @pysnooper.snoop()

# spacer sequence between U6 promoter and sgRNA
# CGAAACACC or CGAAACACCG
key = sys.argv[1]

# dict to list
def dict2list(dic):
    keys = dic.keys()
    values = dic.values()
    return [(key, value) for key, value in zip(keys, values)]

sam = sys.argv[2]

# count of reads without key+sgRNA+scaffold+terminator pattern
no_sgrna = 0

# dict contains all possible transcripts
output = {}

for line in fileinput.input(sam):
    if line[0] != "@":
        line_split = line.split("\t")
        # ref_pos = line_split[3]
        # cigar = line_split[5]
        fastq_seq = line_split[9]

        # sgRNA extraction (18 ~ 22 bp)
        # U6 terminator: TTTTTT
        try:
            sgrna = re.findall(r"%s([ATGC]{0,}?)TTTTTT" %(key), fastq_seq)[0]
        except:
            no_sgrna += 1
        
        # add sgRNA to dict
        try:
            output[sgrna] +=1
        except:
            output[sgrna] = 1
    else:
        continue

# sort dict by count
output_tuple = sorted(dict2list(output), key = lambda x:x[1], reverse=True)

# count of reads without key+sgRNA+scaffold+terminator pattern
print('# Number of reads could not be successfully transcripted: %d' %(no_sgrna))

for i in output_tuple:
    print(i[0] + "\t" + str(i[1]))

