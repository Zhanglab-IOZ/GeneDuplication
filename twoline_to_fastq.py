# usage: python twoline_to_fastq.py --i try.reads.twoline >

# transfer twoline files to fastq file for mapping

from optparse import OptionParser

parser=OptionParser()

parser.add_option('--i', dest='inputsam')

(options, args) = parser.parse_args()

fi=options.inputsam

if __name__ == '__main__':
  fin=open(fi,'r')
  lin=fin.readlines()
  for i in range(len(lin)/2):
    x=lin[2*i+1]
    x1=x.split()
    #print x1; raw_input()
    print '@'+x1[0]
    print x1[1]
    print '+'
    print x1[2]
  
  fin.close()


