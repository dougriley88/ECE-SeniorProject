
class Environment(object):
    '''Manages data and functions to be used by all objects'''
    def __init__(self,time_scale):
        self._ts = time_scale
        
    @property
    def time_scale(self):
        '''The number of seconds represented by a single second of simulation time'''
        return self._ts
    
    ''' setup global dictionary for messages'''
    AppMsg = {'msgTypeMsb':0x0,
                  'msgTypeLsb':0x0,
                  'payloadLen':0x00,
                  'payload':0x0,
                  'checksum':0x0}
    

_environment = None

def setup_environment(time_scale):
    _environment = Environment(time_scale)
    return _environment

