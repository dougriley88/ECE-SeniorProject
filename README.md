# ewhSGDsimulation
Simulation of an electric water heater connected as a Smart Grid Device (SGD)

* Portland State University, Department of Electrical Engineering
* V-Squared, Portland Oregon
* Winter/Spring 2017

This project contains the a program and associated files for the emulation of a water heater that is controlled to support grid conditions.  The water heater in this case supports CTA2045 (formerly USNAP) which is uses a serial interface (SPI) to transfers commands and status between the water heater (the Smart Grid Device, or SGD), and a Universal Communications Module (UCM).  

## Project Setup (Linux)

Requires python 2.7


## Running
```bash
$ cd whSGDemulator/whSGD
$ python main.py --help
```
Simple file i/o is used to emulate the SPI interface where the SGD is the slave, and the UCM is the master.  One file is used for the transfer of bytes from the UCM to the SGD (defaults to mosi.txt), and the other from the SGD to the UCM (defaults to miso.txt).




