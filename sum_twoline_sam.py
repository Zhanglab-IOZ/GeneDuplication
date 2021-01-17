# usage: python sum_twoline_sam.py --i SRR018296.fastq009.sam.reads.twoline --s SRR018296.fastq009.sam.reads.twoline.fastq.sam > SRR018296.fastq009.jump
# now we have two files: the first one is the 'two-line' file, where for
# every read, one line record the raw read and another line record the jump part of this read.
# the second file is a sam file with mapping of the jump part.
# the aim of this script is sum these two files.

# the output file is a sum of reads.
# every read has two lines, the first line is the raw read.
# when a jump part can be uniquely mapped to 2L,2R,3L,3R,X,
# the second line will be sam-format read of the mapped jump part.

from optparse import OptionParser

parser=OptionParser()
parser.add_option('--i', dest='inputtwolinefile')
parser.add_option('--s', dest='samfile')

(options, args) = parser.parse_args()

fi=options.inputtwolinefile
fs=options.samfile

        
if __name__ == '__main__':
    fin = open(fi,'r'); lin = fin.readlines()
    fsin = open(fs,'r'); lsin = fsin.readlines()
    
    lchr=['chr2L','chr2R','chr3L','chr3R','chrX']
    
    if len(lin) > 0:    
        for i in range(len(lin)/2):
            lt1 = lin[2*i]
            lt2 = lin[2*i+1]
            lst = lsin[17+i]
            #print lt1, lt2, lst; raw_input()
            lsts = lst.split()
            
            if lsts[2] in lchr and 'ZS:Z:R' not in lsts and\
                    'ZS:Z:NM' not in lsts and 'ZS:Z:QC' not in lsts:
                print lt1,
                print '\t'.join(lsts)
    
    fin.close()
    fsin.close()


