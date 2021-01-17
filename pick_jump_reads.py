# usage: python pick_jump_reads.py --i SRR058208.fastq011.sam > SRR058208.fastq011.reads
# pick up reads if there's a large soft clip in this read.
# here 'large' means 15 to 70. 
# the reads should be uniquely mapped to the genome and located in
# five main chromosomes.


from optparse import OptionParser

parser=OptionParser()
parser.add_option('--i', dest='inputfile')

(options, args) = parser.parse_args()

fi=options.inputfile


if __name__ == '__main__':
    fin=open(fi,'r')

    l15s70=['20S','21S','22S','23S','24S','25S','26S','27S','28S','29S','30S','31S','32S','33S','34S','35S','36S','37S','38S','39S','40S','41S','42S','43S','44S','45S','46S','47S','48S','49S','50S','51S','52S','53S','54S','55S','56S','57S','58S','59S','60S','61S','62S','63S','64S','65S','66S','67S','68S','69S','70S']
    
    lchr=['chr2L','chr2R','chr3L','chr3R','chrX']

    lin=fin.readline().split()
    while lin:
        if '@SQ' not in lin[0] and '@HD' not in lin[0] and \
                '@PG' not in lin[0]  and lin[2] in lchr and \
                'ZS:Z:R' not in lin and 'ZS:Z:NM' not in lin \
                and 'ZS:Z:QC' not in lin:
            for x in l15s70:
                if x in lin[5]:
                    print '\t'.join(lin)
                    break
        lin=fin.readline().split()

    fin.close()



