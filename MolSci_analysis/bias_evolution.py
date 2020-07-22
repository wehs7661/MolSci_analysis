#!/usr/bin/env python
import os
import argparse
import numpy as np
import matplotlib.pyplot as plt 
from matplotlib import rc

def initialize():

    parser = argparse.ArgumentParser(
        description='This script plot the bias as a function of time for MetaD-EXE.')
    parser.add_argument('--hills',
                        help='The name of PLUMED HILLS file.')
    
    args_parse = parser.parse_args()

    if args_parse.hills is None:
        for file in os.listdir('.'):
            if 'HILLS' in file:
                args_parse.hills = file

    return args_parse

def main():
    rc('font', **{
    'family': 'sans-serif',
    'sans-serif': ['DejaVu Sans'],
    'size': 10
    })
    # Set the font used for MathJax - more on this later
    rc('mathtext', **{'default': 'regular'})
    plt.rc('font', family='serif')

    args = initialize()

    # First parse the PLUMED HILLS file
    t1, h = [], []
    infile = open(args.hills)
    lines = infile.readlines()
    infile.close()

    for line in lines:
        if line[0] != '#':
            t1.append(float(line.split()[0])) # ps
            h.append(float(line.split()[3]))

    plt.figure()
    plt.plot(np.array(t1)/1000, h)
    plt.xlabel('Time (ns)')
    plt.ylabel('Height of the Gaussian biasing potential')
    plt.title('Height of the biasing potential as function of time')
    plt.grid()
    plt.show()


        