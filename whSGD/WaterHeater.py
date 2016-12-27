#!/usr/bin/env python
#---------------------------------------------------------------------------#
# Copyright V-SQUARED, Portland State University. All rights reserved.
#
#    Permission to use, copy, modify, and/or distribute this software for any
#    purpose with or without fee is hereby granted, provided that the above
#    copyright notice and this permission notice appear in all copies.
#
#    THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
#    WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
#    MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
#    ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
#    WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
#    ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
#    OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#---------------------------------------------------------------------------#


__copyright__ = 'Copyright (c) 2016, V-Squared, Portland State University'
__license__ = 'CreativeCommons'

"""PSU Water Heater SGD """
#---------------------------------------------------------------------------# 
# imports
#---------------------------------------------------------------------------#

import sys
from time import sleep
import os
from ConfigParser import ConfigParser



#---------------------------------------------------------------------------#
# Main Script Entry Point
#---------------------------------------------------------------------------#

# Parse the command line arguments

if sys.argv[1] == 'h':
   print "usage: waterheater.py -args"
   print "\t -s scale          integer scale of simulation time to real time, defaults to 300 (1 second equals 5 minutes)":
-i filename       input file name, defaults to mosi.txt
-o filename       output file name, defaults to miso.txt
-b filename       CTA2045 bytecode definitions, defaults to CTA2045.csv
    
   exit()

if not os.path.lexists(sys.argv[1]):
    print "BIS initialization file does not exist: " + sys.argv[1]
    exit()
else:
    bisConfig = open(sys.argv[1],'r')
    line = bisConfig.readline()
    while line:
        if line.startswith('bisName'):
            subline = line.split('=')
            bisName = subline[1].strip('\n')
        if line.startswith('bisPlotFileName'):
            subline = line.split('=')
            bisPlotFileName = subline[1].strip('\n')
        if line.startswith('scale'):
            subline = line.split('=')
            scale = subline[1].strip('\n')
        line = bisConfig.readline()

''' Wait for plotting input file to be created '''
countDown = 20
while not os.path.lexists(bisPlotFileName):
    print "Waiting for plot data file: " + bisPlotFileName
    if countDown == 0:
        print "Plot data file unavailable, exiting...."
        exit()
    else: 
        countDown -= 1
    sleep(5)

''' Initialize figure '''
bisPlotFile = open(bisPlotFileName,'r')

figureTitle = bisName

#Set up one figure for now.  Additional plot areas are added with the 
#subplot cmd. fig is a matplotlib.figure.Figure object

fig,axSOC = plt.subplots(figsize=(5,2),frameon=None)
titletxt = fig.suptitle('SOC', fontsize=14, fontweight='bold')
fig.canvas.set_window_title(figureTitle)

#set plot interactive mode on
plt.ion()

updatePlot(axSOC,bisPlotFile,int(scale))

#cleanup
bisPlotFile.close()


