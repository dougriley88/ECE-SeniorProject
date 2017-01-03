from os import path, mkdir
import csv
import logging

import environment as env

class CTA2045(object):
    '''Emulates the CTA2045 SPI DLL interface'''
    def __init__(self,**kwargs):
        
        '''Manage file I/O'''
        ctaInName = path.join(kwargs['data_directory'],kwargs['CTA2045_in'])
        if not path.lexists(ctaInName):
            logging.error("CTA input file (mosi) does not exist: " + ctaInName)
            exit()
            
        ctaOutName = path.join(kwargs['data_directory'],kwargs['CTA2045_out'])
        
        ctaByteName = path.join(kwargs['data_directory'],kwargs['CTA2045_byte'])
        if not path.lexists(ctaByteName):
            logging.error("CTA byte code file does not exist: " + ctaByteName)
            exit()
        
        ''' file streams should remain open during emulation, so making them global'''
        global ctaIn, ctaOut, msgCodes, ctaDebug
        ctaIn = open(ctaInName,'r')
        ctaOut = open(ctaOutName,'w')
        
        msgCodes = initByteCodes(ctaByteName)
        logging.info("********CTA2045 MESSAGES********")
        for msg in msgCodes:
            logging.info(msg)
        logging.info("********************************")
            
        ctaDebug = (kwargs['CTA2045_debug'])
        
    def cleanup(self):
        logging.info("Cleaning up CTA2045 interface")
        ctaIn.close()
        ctaOut.close()
        
def initByteCodes(ctaByteFile):
    '''Obtains supported byte codes from byte code file'''
    ctaCodes = []
    with open(ctaByteFile) as f:
        reader = csv.DictReader(f)
        for row in reader:
            ctaCodes.append(row)
    f.close()
    return ctaCodes

def checkInterface():
    '''checks for new messages and processes them'''
    msg = (ctaIn.readline()).rstrip('\n')
    appMsg = {}
    while msg:
        appMsg, dllResponse = receiveMsg(msg)
        msg = (ctaIn.readline()).rstrip('\n')
        if dllResponse:
            sendMsg(dllResponse)
        if appMsg:
            '''return to application, we process app messages one at a time '''
            return(appMsg)
    return(appMsg)
    
def receiveMsg(msg):
    mbytes = msg.split(' ')
    appMsg = {}
    dllMsg = []
    
    ''' For app messages, validate the checksum, check payload length'''
    if len(mbytes) > 2:
        if not csCheck(mbytes):
            if ctaDebug:
                logging.info('Message has bad checksum, CTA2045 in debug mode, ignoring error')
            else:
                logging.info('Message has bad checksum, sending DLLNackCS')
                dllMsg = ['15', '03']
                return appMsg,dllMsg
        # remove checksum bytes from msg
        mbytes.pop(); mbytes.pop()
        if not payloadCheck(mbytes):
            logging.info('Message has invalid length, sending DLLNackLen')
            dllMsg = ['15', '02']
            return appMsg,dllMsg
        
    '''Message passes muster, now determine if valid'''    
    
    for row in msgCodes:
        if row['MsgTypeMSB'] == mbytes[0]:
            if row['MsgTypeLSB']== mbytes[1]:
                if len(mbytes) == 2:
                    '''Received a DLL Message'''
                    logging.info('Received '+ row['MsgDesc'] + ': ' + msg)
                    return appMsg,dllMsg
                else:
                    ''' Received an Application Message'''
                    ''' Check for supported message '''
                    # TODO: Extend for intermediate DR, and app query as needed
                    if row['MsgType'] == 'BasicDR' and row['Opcode1'] == mbytes[4]:
                        logging.info('Received message:' + row['MsgName'] + ', Opcode2:' + mbytes[5])
                        dllMsg = ['06','02']
                        appMsg['MsgName'] = row['MsgName']
                        appMsg['MsgType'] = row['MsgType']
                        appMsg['Opcode1'] = mbytes[4]
                        appMsg['Opcode2'] = mbytes[5]
                        return appMsg,dllMsg
    
    ''' Fall-thru, no valid message match'''
    logging.info('Unsupported or invalid message, sending DLLNack')
    dllMsg = ['15', '02']
    return appMsg, dllMsg                                       
        
def csCheck(msgBytes):
    cb1 = 0xaa
    cb2 = 0x0
    for byte in msgBytes:
        hex_byte = int(byte,16)
        cb1 = (cb1 + hex_byte)%255
        cb2 = (cb2 + cb1)%255
    if ((cb1 == 0) and (cb2==0)):
        return True
    else:
        return False
    
def csCalc(msgBytes):
    cb1 = 0xaa
    cb2 = 0x0
    for byte in msgBytes:
        cb1 = (cb1 + int(byte,16))%255
        cb2 = (cb2 + cb1)%255
    mscb = 255 - ((cb1+cb2)%255)
    lscb = 255 - ((cb1+mscb)%255)
    return format(mscb,'02x'),format(lscb,'02x')
        
def payloadCheck(msgBytes):
    if len(msgBytes) < 4:
        return False
    payloadLen = int(msgBytes[2],16) + int(msgBytes[3],16)
    msgPayload = len(msgBytes)- 4
    if (payloadLen != msgPayload):
        return False
    else:
        return True
    
def sendMsg(byteList):
    ''' byteList contains a list of 2 digit hex byte values '''
    outstr = ""
    for byte in byteList:
        outstr = outstr + byte + ' '
    ctaOut.write(outstr + '\n')
        
def sendAppMsg(msg):  
    ''' converts an application message for sending to DLL '''
    if not msg:
        logging.error('Send application message error: empty message')
        return
   
    msgBytes = []
    for row in msgCodes:
        if msg['MsgName'] == row['MsgName']:
            '''Valid message'''
            msgBytes = [row['MsgTypeMSB'],row['MsgTypeLSB']]
            if row['MsgType'] == 'BasicDR':
                '''Add payload length'''
                msgBytes = msgBytes + ['00', '02']
            else: 
                logging.error("Application Message Send error, unsupported type " + row['MsgTYpe'])
                return
            ''' Add opcodes '''
            msgBytes = msgBytes + [row['Opcode1'], msg['Opcode2']]
            ''' Add Checksum '''
            mscb, lscb = csCalc(msgBytes)
            logging.info("Sending Application Message: " + msg['MsgName'] )            
            msgBytes = msgBytes + [mscb,lscb]
            sendMsg(msgBytes)
            return
    ''' Message not found'''
    logging.error("Application Message Send error, invalid name " + msg['MsgName'])
    
        
    
        
        