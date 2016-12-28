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

import sys
from os import path, mkdir
import logging
import pprint
import time


import argparse
import whemulator

def main():
    emu = whemulator.Emu(**vars(parse_args()))
    emu.run()

def parse_args():
    '''Parses command line arguments'''
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    #Set up all of the available arguments and defaults
    parser.add_argument("--time_scale",
        dest="time_scale",
        default=300,
        help="emulation time scale",
        metavar="TS",
        type=int)
    parser.add_argument("--run_time",
        dest="run_time",
        default=20,
        help="emulation run time in seconds",
        metavar="RUNTIME",
        type=int)
    parser.add_argument("--data_dir",
        help="Directory containing input data files",
        dest="data_directory",
        default="../data/",
        metavar="DIRECTORY",
        type=str)
    parser.add_argument("--log-file",
        help="log file name",
        default="wh_emulation.log",
        metavar='OUTPUT_LOG',
        type=str)
    parser.add_argument("--CTA2045_in",
        help="CTA 2045 input file name",
        dest="CTA2045_in",
        default='mosi.txt',
        type=str)
    parser.add_argument("--CTA2045_out",
        help="CTA 2045 output file name",
        dest="CTA2045_out",
        default='miso.txt',
        type=str)
    parser.add_argument("--CTA2045_byte",
        help="CTA 2045 byte code file name",
        dest="CTA2045_byte",
        default='miso.txt',
        type=str) 

    # Get and process the args
    args = parser.parse_args()

    if not path.isdir(args.data_directory):
        parser.error("Directory '{0}' does not exist.".format(args.data_directory))
        sys.exit(1)

    # Clear the log file
    with open(args.log_file,'w'):
        pass

    logging.basicConfig(filename=args.log_file,level='DEBUG')
    logging.info("-----CTA2045 Water Heater Emulation starting at {0}-----".format(time.strftime('%X %x %Z')))
    logging.info("Arguments: {0}".format(pprint.pformat(args)))

    return args

if __name__ == '__main__':
    main()

    
      
        
   




