
# usage: python clustering_exhausting.py --i 304.ar.kind-23.cln.bed.sorted --t PE --d ta
# --t: type. two types: PE, SR
# --d: duplication type. two types: di (dispersed), ta (tandem)

from optparse import OptionParser

parser=OptionParser()
parser.add_option('--i', dest='inputfile')
parser.add_option('--t', dest='filetype')
parser.add_option('--d', dest='duplicationtype')

(options, args) = parser.parse_args()

fi = options.inputfile
ftype = options.filetype
dtype = options.duplicationtype

def handlelpr(lt):
    
    if dtype == 'ta':
        bp_1 = []
        for x in lt:
            bp_1.append(int(x[1])); bp_1.append(int(x[4]))
        bp_1.sort()
        
        lo = lt[0]
        print 'tandem' + '\t' + lo[0] + '\t' + str(bp_1[0]) + '\t' + str(bp_1[-1]) + '\t' + str(len(lt))
        for x in lt:
            print '\t'.join(x)
        #raw_input()
    
    return ''
    
if __name__ == '__main__':
    fin = open(fi,'r')
    lin = fin.readlines()
    
    #print len(lin)
    
    while len(lin) > 0:
        
        lcom = lin[0].split()
        del lin[0]
        
        l_overlap = []
        l_remain = []
        l_overlap.append(lcom)
        for i in range(len(lin)):
            lt = lin[i].split()
            if ftype == 'PE':
                if lt[0] == lcom[0] and lt[3] == lcom[3] and \
                        abs(int(lt[1])-int(lcom[1])) < 500 and \
                        abs(int(lt[4])-int(lcom[4])) < 500:
                    l_overlap.append(lt)
                    
                
                elif lt[0] == lcom[3] and lt[3] == lcom[0] and \
                        abs(int(lt[1])-int(lcom[4])) < 500 and \
                        abs(int(lt[4])-int(lcom[1])) < 500:
                    l_overlap.append(lt)
                    
                else: l_remain.append('\t'.join(lt))
                        
            if ftype == 'SR':
                if lt[0] == lcom[0] and lt[3] == lcom[3] and \
                        abs(int(lt[1])-int(lcom[1])) < 50 and \
                        abs(int(lt[4])-int(lcom[4])) < 50:
                    l_overlap.append(lt)

                
                elif lt[0] == lcom[3] and lt[3] == lcom[0] and \
                        abs(int(lt[1])-int(lcom[4])) < 50 and \
                        abs(int(lt[4])-int(lcom[1])) < 50:
                    l_overlap.append(lt)
                    
                else: l_remain.append('\t'.join(lt))
                
        #print len(l_remain), len(l_overlap); raw_input()
        
        if len(l_overlap) > 2:
            handlelpr(l_overlap)
        
        lin[:] = l_remain[:]
        
        
        
            
    fin.close()

