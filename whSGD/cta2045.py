from os import path, mkdir
import csv

class CTA2045(object):
    '''Emulates the CTA2045 SPI interface'''
    def __init__(self,**kwargs):
        
        '''Manage file I/O'''
        ctaInName = path.join(kwargs['data_dir'],kwargs['CTA2045_in'])
        if not os.path.lexists(ctaInName):
            logging.error("CTA input file (mosi) does not exist: " + ctaInName)
            exit()
        
        ctaByteName = path.join(kwargs['data_dir'],kwargs['CTA2045_byte'])
        if not os.path.lexists(ctaByteName):
            logging.error("CTA byte code file does not exist: " + ctaByteName)
            exit()
        
        ctaIn = open(ctaInName,'r')
        ctaOut = open(ctaOutName,'w')
        ctaByteCode = initByteCodes(ctaByteName)
        
def initByteCodes(ctaByteName):
    '''Obtains supported byte codes from byte code file'''
    bytecode = open(ctaByteName,'r')
    line = bytecode.readline()
    while line:
        print line
        line = bytecode.readline()
    return TRUE

def cleanup():
    ctaIn.close()
    ctaOut.close()
     
        
        
        
        