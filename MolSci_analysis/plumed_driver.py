#!/usr/bin/env python
"""This is a Python script for parsing the output of plumed driver and plotting
the time-series data.
"""

import argparse
import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib import rc

def initialize():

    parser = argparse.ArgumentParser(
        description='This script parses the output of plumed driver and plots \
                     the time-series data.')
    parser.add_argument('-i',
                        '--dat',
                        help='The file name of the plumed output file.')
    parser.add_argument('-x',
                        '--xlabel',
                        default='Time (ns)',
                        help='The name and units of x-axis.')
    parser.add_argument('-y',
                        '--ylabel',
                        help='The name and units of y-axis.')
    parser.add_argument('-l',
                        '--legends',
                        nargs='+',
                        help='The name of the legends.')
    parser.add_argument('-t',
                        '--title',
                        help='The title of the plot.')
    parser.add_argument('-n',
                        '--pngname',
                        help='The filename of the figure.')
    parser.add_argument('-ts',
                        '--timestep',
                        default=1,
                        help='The timestep in the MD simulation')

    args_parse = parser.parse_args()
    
    if args_parse.pngname is None and args_parse.ylabel is not None:
        args_parse.pngname = args_parse.ylabel.split('(')[0]

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

    # Part 1: Parse the file
    x, y = [], []
    infile = open(args.dat)
    lines = infile.readlines()
    infile.close

    line_n = 0
    for line in lines:
        line_n += 1
        if '#! FIELDS' in line:   # lines[line_n - 1]
            variables = line.split('FIELDS')[1].split()
            n_vars = len(variables)  # min of n_vars: 2 (x and y)

            if n_vars > 2:        # multiple y variables
                for i in range(n_vars - 1):  # not including x
                    y.append([])
            break
        
    for line in lines[line_n:]:
        if line[0] != 'P' and line[0] != '#':     # in case of including "PLUMED:   "
            data = line.split()
            x.append(float(data[0]))

            if n_vars == 2:
                y.append(float(data[1]))
            else:
                for i in range(n_vars - 1):
                    y[i].append(float(data[i + 1]))

    x, y = np.array(x), np.array(y)
    if variables[0] == 'time':
        x /= 1000     # convert from ps to ns
        x *= float(args.timestep)

    # Part 2: Some simple data anaylsis
    if args.ylabel is not None and '(' in args.ylabel:  # '(' in ylabel -> y has units
        y_unit = args.ylabel.split('(')[1].split(')')[0]
    else:
        y_unit = ""

    result_str = 'Data analysis of the file %s:' % args.dat 
    print(result_str)
    print('=' * len(result_str))
    if n_vars == 2:
        y_avg = np.mean(y)
        y2_avg = np.mean(np.power(y, 2))
        RMSF = np.sqrt((y2_avg - y_avg ** 2)) / y_avg
        print('The average of %s: %5.3f %s (RMSF: %5.3f %s max: %5.3f %s, min: %5.3f %s)' %(variables[1], np.mean(y), y_unit, RMSF, y_unit, np.max(y), y_unit, np.min(y), y_unit))
        y = list(y)
        print('The maximum occurs at %s ns, while the minimum occurs at %s ns.' %(x[y.index(max(y))], x[y.index(min(y))]))
        y = np.array(y)
    else:
        for i in range(n_vars - 1):
            y_avg = np.mean(y[i])
            y2_avg = np.mean(np.power(y[i], 2))
            RMSF = np.sqrt((y2_avg - y_avg ** 2)) / y_avg
            print('The average of %s: %5.3f %s (RMSF: %5.3f %s max: %5.3f %s, min: %5.3f %s)' %(variables[i + 1], np.mean(y[i]), y_unit, RMSF, y_unit, np.max(y[i]), y_unit, np.min(y[i]), y_unit))

    # Part 3: Plot and save the figure
    plt.figure()
    if n_vars == 2:
        plt.plot(x, y)
    else:
        for i in range(n_vars - 1):
            if i == 0:
                plt.plot(x, y[0])
                plt.ylim([0, 8])

            """
            if args.legends is not None:
                plt.plot(x, y[i], label='%s' % args.legends[i])
            else:
                plt.plot(x, y[i], label='%s' % variables[i + 1])
            plt.legend()    
            """        
    
    plt.xlabel('%s' % args.xlabel)
    plt.ylabel('%s' % args.ylabel)
    if args.title is not None:
        plt.title('%s' % args.title)

    if max(abs(x)) > 10000 or max(abs(x)) < 0.0001:
        plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))

    if n_vars == 2:
        if max(abs(y)) > 10000 or max(abs(y)) < 0.0001:
            plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
    else:
        for i in range(n_vars - 1):
            if max(abs(y[i])) > 10000 or max(abs(y[i])) < 0.0001:
                plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
                break

    plt.grid()

    plt.savefig('%s.png' % args.pngname)
    plt.show()

    delta2 = np.power(y[0] - y[1], 2)
    #RMSD = np.sqrt(np.sum(delta2) / len(delta2))
