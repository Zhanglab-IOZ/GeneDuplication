# GeneDuplication
In-house scripts and pipeline of the gene duplication project.

This is pipeline for our own split-read process.

1, align by novoalign
/home/lleng/program/novoalign/novocraft/novoalign -f SRR058286.fastq011 -d /home/lleng/program/novoalign/ref/dna_ensembl/dmel_ensembl75_dna.nix -o SAM -r Random -R 10 >  SRR058286.fastq011.sam 2> SRR058286.fastq011err.try.log

2, pick jumping reads
Pick reads if there's a large soft clip in this read, where 'large' means the soft-clip part is larger than 20 bp.  The reads should be uniquely mapped to the genome and located in five main chromosomes. 

python pick_jump_reads.py --i SRR058208.fastq011.sam > SRR058208.fastq011.reads


3, map jump part
The jumping reads should have a large soft-clip part. if there's two soft-clip parts, this read will be abandoned. The input file is a sam file. the output file will be an expanded sam file that every read has two lines: the first line is the sam-format raw read, the second line has a format like this:
SRR058208.11076897_16_16S20M    TTTGTCCCTTGGTTTT        2757730377+/).0+
read name + flag + cigar, sequence, quality

python twoline_to_fastq.py --i SRR058208.fastq011.reads.twoline > SRR058208.fastq011.reads.twoline.fastq

/home/lleng/program/novoalign/novocraft/novoalign -f SRR001935.fastq000.sam.reads.twoline.fastq -d /home/lleng/program/novoalign/ref/dna_ensembl/dmel_ensembl75_dna.nix -o SAM -r Random -R 10  > ../sams/SRR001935.fastq000.sam.reads.twoline.fastq.sam 2> SRR001935.fastq000.sam.reads.twoline.fastqerr.try.log

4, sum raw read and mapped jump part
Now we have two files: the first one is the 'two-line' file, where for every read one line record the raw read and another line record the jump part of this read. The second file is a sam file with mapping of the jump part. Then a script is used to sum these two files. In the output file, every qualified read, i.e. the jump part can also be uniquely mapped to some place of 5 main chromosomes, has two lines. The first line is the raw read, the second line will be sam-format read of the mapped jump part.

python sum_twoline_sam.py --i SRR018296.fastq009.sam.reads.twoline --s SRR018296.fastq009.sam.reads.twoline.fastq.sam > SRR018296.fastq009.jump

5, clustering split-read pair to call duplication
For detail about bedPE format see 
http://bedtools.readthedocs.org/en/latest/content/general-usage.html

for i in `ls *cln`; do python ~/src/splitread_bed.py --i $i > ../k3-bed/$i.bed; done
for i in `ls *bed`; do sort -k1,1 -k2,2n $i > $i.sorted; done
for i in `ls *ar*sorted`; do python ~/src/clustering_exhausting.py --i $i > $i.td ; done
for i in `ls *td`; do cat $i | grep tan | awk '{print $2"\t"$3"\t"$4}' > $i.bed; done
for i in `ls *bed`; do python ~/src/bed_filtering.py --i $i > $i.cln; done
for i in `ls *cln`; do awk '{a=$3-$2}{print $1"\t"$2"\t"$3"\t"a}' $i > $i.t; done
for i in `ls *.t`; do sort -k4,4n $i > $i.sorted; done


