#!/usr/bin/env python
"""This is a Python script for parsing PLUMED output file, COLVAR, and plot the 
histogram of the discrete collective variables. 
"""

import argparse
import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib import rc 
from collections import OrderedDict

def initialize():
    
    parser = argparse.ArgumentParser(
        description='This script parses PLUMED output file, COLVAR, and plot the\
        histogram of the discrete collective variables.')
    parser.add_argument('-i',
                        '--dat',
                        help='The file name of the PLUMED output file.')
    parser.add_argument('-x',
                        '--xlabel',
                        help='The name and units of x-axis.')
    parser.add_argument('-y',
                        '--ylabel',
                        help='The name and units of y-axis.')
    parser.add_argument('-t',
                        '--title',
                        help='The title of the plot.')
    parser.add_argument('-n',
                        '--pngname',
                        default='Final_hist_COLVAR.png',
                        help='The filename of the figure.')

    args_parse = parser.parse_args()

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

    time, data, counts = [], [], {}
    infile = open(args.dat)
    lines = infile.readlines()
    infile.close

    line_n = 0
    for line in lines:
        line_n += 1
        if line[0] != '#':
            if float(line.split()[0]) != 0:
                time.append(float(line.split()[0]))
                data.append(float(line.split()[1]))
    
    examined_CV = []
    for i in data:
        if i not in examined_CV:
            examined_CV.append(i)
            counts[f'{int(i)}'] = data.count(i)
    counts = OrderedDict(sorted(counts.items()))

    # Plot the final histogram
    plt.figure()
    plt.bar(list(counts.keys()), height=list(counts.values()))
    plt.xlabel('States')
    plt.ylabel('Counts')
    plt.minorticks_on()
    plt.title(f'The final histogram of the simulation (at {max(time) / 1000} ns)')
    if max(list(counts.values())) >= 10000:
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
    plt.grid()
    plt.savefig(args.pngname, dpi=600)
    
