# usage: python divide_read_jump.py --i try.reads > try.reads.twoline
# 1, the read should have a large soft-clip part. if there's two soft-clip parts, this read
# will be abondoned.   
# 2, the input file is a sam file. the output file will be an expanded sam file that every read has two lines:
# the first line is the sam-format read, the second line has a format like this:
# SRR058208.11076897_16_16S20M    TTTGTCCCTTGGTTTT        2757730377+/).0+
# read name + flag + cigar, sequence, quality 

from optparse import OptionParser

parser=OptionParser()

parser.add_option('--i', dest='inputsam')

(options, args) = parser.parse_args()

fi=options.inputsam

def complseq(lt1):
  #print lt1
  lt2 = lt1[::-1]#; print lt2; raw_input()
  lt3='';
  for x in lt2:
    if x == 'A': lt3 = lt3 + 'T'
    elif x == 'T': lt3 = lt3 + 'A'
    elif x == 'C': lt3 = lt3 + 'G'
    elif x == 'G': lt3 = lt3 + 'C'
    else: lt3 = lt3 + x
  #print lt3; raw_input()
  return lt3

def printsc(l1):
  #print l1;raw_input()
  locs1=[];locs2=[];cigar=l1[5]
  #print cigar; raw_input()
  if ( cigar[2] == 'S' and cigar[:2].isdigit() ):
    locs1 = cigar[:3]
  elif ( cigar[3] == 'S' and cigar[:3].isdigit() ):
    locs1 = cigar[:4]
  
  if ( cigar[-1] == 'S' and cigar[-3:-1].isdigit() and cigar[-4].isalpha() ):
    locs2 = cigar[-3:]
  elif ( cigar[-1] == 'S' and cigar[-4:-1].isdigit() ):
    locs2 = cigar[-4:]
  
  lo=[]
  #print locs1, locs2; raw_input()
  if locs1 and locs2:
    #print locs1, locs2, 'hello'; raw_input()
    return 
  elif locs1:
    #print locs1, l1; raw_input()
    lensp = int(locs1[:-1]) #; print lensp; raw_input()
    lo.append(l1[0]+'_'+l1[1]+'_'+l1[5])
    if int(l1[1]) & 0x10 == 0: # strand +
      lt=l1[9]; lo.append(lt[:lensp])
      lt=l1[10]; lo.append(lt[:lensp])
    else: # strand -
      lt=l1[9]; lt1=lt[:lensp]; lo.append(complseq(lt1))
      lt=l1[10]; lt1=lt[:lensp]; lo.append(lt1[::-1])
  elif locs2:
    lensp = int(locs2[:-1])
    lo.append(l1[0]+'_'+l1[1]+'_'+l1[5])
    if int(l1[1]) & 0x10 == 0: 
      lt=l1[9]; lensp1 = -1 * lensp ; lo.append(lt[lensp1:])
      lt=l1[10]; lo.append(lt[lensp1:])
    else:
      lt=l1[9]; lensp1 = -1 * lensp; lt1=lt[lensp1:]; lo.append(complseq(lt1))
      lt=l1[10]; lt1=lt[lensp1:]; lo.append(lt1[::-1])

  return lo 

if __name__ == '__main__':
  fin=open(fi,'r')
  lin=fin.readlines()
  for x in lin:
    x1=x.split()
    psc=printsc(x1)
    if psc:
      print '\t'.join(x1)
      print '\t'.join(psc) #; raw_input()
    
  fin.close()


