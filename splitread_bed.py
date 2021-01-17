#
# For detail about bedPE format see 
# http://bedtools.readthedocs.org/en/latest/content/general-usage.html

# order for split-read jumping pairs:
# chrom1    breakpoint_1    coordinate_1    chrom2  breakpoint_2    coordinate_2
# name  score   strand_1    strand_2
# scores are artificially set to 99
# coordinate comes directly from sam-format reads

from optparse import OptionParser

parser=OptionParser()
parser.add_option('--i', dest='inputfile')

(options, args) = parser.parse_args()

fi=options.inputfile

def getstrapos(l1,l2):

    if int(l1[1]) & 0x10 == 0: # the main read is in the forward strand
        lcigar = l1[5]
        breakpoint_1 = 0
        if lcigar[-1] == 'S' and lcigar[-4].isalpha() and lcigar[-3:-1].isdigit():
            breakpoint_1 = int(l1[3]) + len(l1[9])-int(lcigar[-3:-1])
            
            if int(l2[1]) & 0x10 == 0: breakpoint_2 = int(l2[3])
            else: breakpoint_2 = int(l2[3]) + len(l2[9])
            
        elif lcigar[-1] == 'S' and lcigar[-5].isalpha() and lcigar[-4:-1].isdigit():
            breakpoint_1 = int(l1[3]) + len(l1[9])-int(lcigar[-4:-1])
            
            if int(l2[1]) & 0x10 == 0: breakpoint_2 = int(l2[3])
            else: breakpoint_2 = int(l2[3]) + len(l2[9])        
        
        if breakpoint_1 == 0:
            
            if lcigar[2] == 'S' and lcigar[:2].isdigit():
                breakpoint_1 = int(l1[3])
                
                if int(l2[1]) & 0x10 == 0: breakpoint_2 = int(l2[3]) + len(l2[9])
                else: breakpoint_2 = int(l2[3]) 
                
            elif lcigar[3] == 'S' and lcigar[:3].isdigit():
                breakpoint_1 = int(l1[3])            

                if int(l2[1]) & 0x10 == 0: breakpoint_2 = int(l2[3]) + len(l2[9])
                else: breakpoint_2 = int(l2[3]) 
        
        """
        if breakpoint_1 != 0 and int(l2[1]) & 0x10 == 0:
            breakpoint_2 = int(l2[3]) + len(l2[9])
        else:
            breakpoint_2 = int(l2[3])
        """
        
        if int(l1[1]) & 0x10 == 0: strand_1 = '+'            
        else: strand_1 = '-'
        
        if int(l2[1]) & 0x10 == 0: strand_2 = '+'            
        else: strand_2 = '-'                

        print lt1[2] + '\t' + str(breakpoint_1) + '\t' + lt1[3] + '\t' + lt2[2] + '\t' + str(breakpoint_2) + '\t'+lt2[3] + '\t'+ lt1[0] + '\t99\t'+strand_1+'\t'+strand_2
        
        return ''
    
    if int(l1[1]) & 0x10 != 0:
        lcigar = l1[5]
        breakpoint_1 = 0
        if lcigar[2] == 'S' and lcigar[:2].isdigit():
            breakpoint_1 = int(l1[3])

            if int(l2[1]) & 0x10 == 0: breakpoint_2 = int(l2[3])
            else: breakpoint_2 = int(l2[3]) + len(l2[9])
                
        elif lcigar[3] == 'S' and lcigar[:3].isdigit():
            breakpoint_1 = int(l1[3])

            if int(l2[1]) & 0x10 == 0: breakpoint_2 = int(l2[3])
            else: breakpoint_2 = int(l2[3]) + len(l2[9])
        
        if breakpoint_1 == 0:

            if lcigar[-1] == 'S' and lcigar[-4].isalpha() and lcigar[-3:-1].isdigit():
                breakpoint_1 = int(l1[3]) + len(l1[9])-int(lcigar[-3:-1])
                
                if int(l2[1]) & 0x10 == 0: breakpoint_2 = int(l2[3]) + len(l2[9])  
                else: breakpoint_2 = int(l2[3])              
                
            elif lcigar[-1] == 'S' and lcigar[-5].isalpha() and lcigar[-4:-1].isdigit():
                breakpoint_1 = int(l1[3]) + len(l1[9])-int(lcigar[-4:-1])            
        
                if int(l2[1]) & 0x10 == 0: breakpoint_2 = int(l2[3]) + len(l2[9])  
                else: breakpoint_2 = int(l2[3])       
        
        """
        if breakpoint_1 != 0  and int(l2[1]) & 0x10 != 0:
            breakpoint_2 = int(l2[3])
        else:
            breakpoint_2 = int(l2[3]) + len(l2[9])
        """
        if int(l1[1]) & 0x10 == 0: strand_1 = '+'            
        else: strand_1 = '-'
        
        if int(l2[1]) & 0x10 == 0: strand_2 = '+'            
        else: strand_2 = '-'               

        print lt1[2] + '\t' + str(breakpoint_1) + '\t' + lt1[3] + '\t' + lt2[2] + '\t' + str(breakpoint_2) + '\t'+lt2[3] + '\t'+ lt1[0] + '\t99\t'+strand_1+'\t'+strand_2          
        
        return ''

if __name__ == '__main__':
    fin=open(fi,'r')
    lin=fin.readlines()
    
    for i in range(len(lin)/2):
        lt1 = lin[2*i].split(); lt2 = lin[2*i + 1].split()
        
        strapos = getstrapos(lt1, lt2)
        
        
    fin.close()
    
