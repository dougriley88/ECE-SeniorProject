
import logging
import whmodel

import environment as env

class WaterHeater(object):
    '''Emulates the WaterHeater Application layer'''
    def __init__(self,**kwargs):
        
        logging.info("Initializing Water Heater Aplication")
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
    return {}


                
        
    
        
        
