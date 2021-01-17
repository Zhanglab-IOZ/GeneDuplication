# GeneDuplication
In-house pipeline of the gene duplication project.

This is the pipeline for our own split-read based calling process.

1, align by novoalign


/home/lleng/program/novoalign/novocraft/novoalign -f SRR058286.fastq011 -d /home/lleng/program/novoalign/ref/dna_ensembl/dmel_ensembl75_dna.nix -o SAM -r Random -R 10 >  SRR058286.fastq011.sam 2> SRR058286.fastq011.err.log

2, pick jumping or split reads


Pick reads if there's a large soft clip in this read, where 'large' means the soft-clip part is larger than 20 bp.  The reads should be uniquely mapped to the genome and located in five major chromosomes. 

python pick_jump_reads.py --i SRR058286.fastq011.sam > SRR058286.fastq011.reads


3, map jumping part


The split reads should have a large soft-clip part. If there's two soft-clip parts, this read will be abandoned. The input file is a sam file. the output file will be an expanded sam file that every read has two lines: the first line is the sam-format raw read, the second line has a format like this:
SRR058208.11076897_16_16S20M    TTTGTCCCTTGGTTTT        2757730377+/).0+

read name + flag + cigar, sequence, quality

python divide_read_jump.py --i SRR058286.fastq011.reads > SRR058286.fastq011.reads.twoline

python twoline_to_fastq.py --i SRR058286.fastq011.reads.twoline > SRR058286.fastq011.reads.twoline.fastq

/home/lleng/program/novoalign/novocraft/novoalign -f SRR058286.fastq011.reads.twoline.fastq -d /home/lleng/program/novoalign/ref/dna_ensembl/dmel_ensembl75_dna.nix -o SAM -r Random -R 10  > ../sams/SRR058286.fastq011.reads.twoline.fastq.sam 2> SRR058286.fastq011.reads.twoline.fastq.err.log

4, merge raw read and mapped jumping part


Now we have two files: the first one is the 'two-line' file, where for every read one line record the raw read and another line record the jumping part of this read. The second file is a sam file with mapping of the jumping part. Then a script is used to merge these two files. In the output file, every qualified read, i.e. the jumping part can also be uniquely mapped to some place of 5 main chromosomes, has two lines. The first line is the raw read, the second line will be sam-format read of the mapped jumping part.

python sum_twoline_sam.py --i SRR058286.fastq011.reads.twoline --s SRR058286.fastq011.reads.twoline.fastq.sam > SRR058286.fastq011.jump

5, clustering split-read pairs to call duplication


for i in `ls *jump`; do python ~/src/splitread_bed.py --i $i > ../k3-bed/$i.bed; done

for i in `ls *bed`; do python ~/src/clustering_exhausting.py --i $i > $i.td ; done


The final *.td file then store tandem duplication calls for following analysis. For example, the bed_filtering.py could be used to check and filter unexpected call whose length is not as long as pre-defined by us. 

