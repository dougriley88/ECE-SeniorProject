#******************************************************************************
# Copyright (c) 2016, V-SQUARED, Portland State University
# All rights reserved.
#
#   Permission to use, copy, modify, and/or distribute this software for any
#   purpose with or without fee is hereby granted, provided that the above
#   copyright notice and this permission notice appear in all copies.
#
#   THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
#   WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
#   MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
#   ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
#   WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
#   ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
#   OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#******************************************************************************
__copyright__ = 'Copyright (c) 2016, V-Squared, Portland State University'
__license__ = 'CreativeCommons'

import logging
import time

import environment
import cta2045
import waterheater as wh



class Emu(object):
    ''' Water Heater Emulator '''
    def __init__(self, **kwargs):
        
        self.run_time = (kwargs['run_time'])
        # Set up emulation environment
        env_args = (kwargs['time_scale'])
        self._environment = environment.setup_environment(env_args)

        # Set up CTA 2045 interface
        self.ctaInterface= cta2045.CTA2045(**kwargs)
        self.wh = wh.WaterHeater(**kwargs)

    def run(self):
        try:
            for time_step in range(1,self.run_time):
                self.do_timestep(time_step)
        except KeyboardInterrupt:
            logging.info('Emulation Interrupted')
            pass
        finally:
            '''close up shop '''
            self.ctaInterface.cleanup()

    def do_timestep(self,time_step):
        logging.info('Emulation seconds: {0}'.format(time_step))
        appMsg = cta2045.checkInterface()
        appResp = wh.update(appMsg)
        if appResp:
            cta2045.sendAppMsg(appResp)
        time.sleep(1)  
        

