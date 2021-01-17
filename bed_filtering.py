

from optparse import OptionParser

parser=OptionParser()

parser.add_option('--i', dest='inputsam')

(options, args) = parser.parse_args()

fi=options.inputsam

def handle(lpr):
    #print lpr ; raw_input()
    
    bp_1 = []
    for x in lpr:
        bp_1.append(int(x[1])); bp_1.append(int(x[2]))
    bp_1.sort()
    
    lo = lpr[0]
    print lo[0] + '\t' + str(bp_1[0]) + '\t' + str(bp_1[-1])
    
if __name__ == '__main__':
    fin=open(fi,'r')
    lin=fin.readline().split()
    
    lt=lin[:]
    lpr=[]
    """
    if lin[0] == lt[0] and (((int(lin[2]) > int(lt[2])) and (int(lin[1]) < int(lt[2]))) or \
                ((int(lin[2]) > int(lt[1])) and (int(lin[1]) < int(lt[1]))) or
                ((int(lin[2]) > int(lt[2])) and (int(lin[1]) < int(lt[1]))) or
                ((int(lin[2]) < int(lt[2])) and (int(lin[1]) > int(lt[1])))
                ):
        pass
    else:
        print '\t'.join(lin)
    """
    lin=fin.readline().split()
    while lin:

        if lin[0] == lt[0] and (((int(lin[2]) > int(lt[2])) and (int(lin[1]) < int(lt[2]))) or \
                ((int(lin[2]) > int(lt[1])) and (int(lin[1]) < int(lt[1]))) or
                ((int(lin[2]) > int(lt[2])) and (int(lin[1]) < int(lt[1]))) or
                ((int(lin[2]) < int(lt[2])) and (int(lin[1]) > int(lt[1])))
                ):
            if len(lpr) == 0:
                lpr.append(lt)
                lpr.append(lin)
            else:
                lpr.append(lin)
            
        else:
            if len(lpr) != 0:
                handle(lpr)
                #raw_input()
                lpr=[]
            else:
                print '\t'.join(lt)
            
                
        lt=lin[:]
        lin=fin.readline().split()
    
    print '\t'.join(lt) 
       
    fin.close()

