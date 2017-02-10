
import logging
import whmodel

import environment as env

class WaterHeater(object):
    '''Emulates the WaterHeater Application layer'''
    def __init__(self,**kwargs):
        
        logging.info("Initializing Water Heater Application")
        self.whmodel = whmodel.WHModel(**kwargs)
        
        
def update(appMsg):
    '''Water heater timestep entry point'''
    '''process new application message if valid'''
    appResp = {}
    if appMsg:
        appResp = handleMsg(appMsg)   
    whmodel.updateState()
    return (appResp)

def handleMsg(appMsg):
    ''' Handles the message and generates a response message to send'''
    #TODO: Add Code here for handling message
    appResp = {'MsgName':'AppAck','Opcode2':appMsg['Opcode1']}
    return appResp


                
        
    
        
        
