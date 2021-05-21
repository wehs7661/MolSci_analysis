#!/usr/bin/env python
"""This is a Python code for the plotting of 2-dimensional data.
"""
import natsort
import argparse
import os.path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc


def initialize():

    parser = argparse.ArgumentParser(
        description='This code saves a contour plot based on 3-dimensional data')
    parser.add_argument('-f',
                        '--xvg',
                        nargs='+',
                        help='Names of the input .xvg files')
    parser.add_argument('-l',
                        '--legend',
                        nargs='+',
                        help='Legends of the curves')
    parser.add_argument('-x',
                        '--xlabel',
                        type=str,
                        help='The name and units of x-axis')
    parser.add_argument('-y',
                        '--ylabel',
                        type=str,
                        default='Count',
                        help='The name and units of y-axis')
    parser.add_argument('-c', 
                        '--column', 
                        type=int, 
                        default=1,
                        help='The column index of the dependent variable.')
    parser.add_argument('-t', 
                        '--title', 
                        type=str, 
                        help='Title of the plot')
    parser.add_argument('-n',
                        '--pngname',
                        type=str,
                        help='The filename of the figure, not including the extension')
    parser.add_argument('-nb',
                        '--nbins',
                        type=int,
                        default=200,
                        help='The number of bins for the histogram.')
    parser.add_argument('-cc',
                        '--conversion',
                        choices=['degree to radian', 'radian to degree', 'kT to kcal/mol', 'kcal/mol to kT', 'kT to kJ/mol', 'kJ/mol to kT', 'kJ/mol to kcal/mol', 'kcal/mol to kJ/mol', 'ns to ps', 'ps to ns'],
                        help='The unit conversion for the data in x-axis.')
    parser.add_argument('-ff',
                        '--factor',
                        type=float,
                        help='The factor to be multiplied to the x values of the histogram.')
    parser.add_argument('-T',
                        '--temp',
                        help='Temperature for unit convesion involving kT. Default: 298.15.')
    parser.add_argument('-o',
                        '--outline',
                        default=False,
                        action='store_true',
                        help='Whether to plot the histogram outline.')
    parser.add_argument('-tr',
                        '--truncate',
                        help='-tr 1 means truncate the first 1%% of the data.')
    parser.add_argument('-Nb',
                        '--Nr_bound',
                        type=float,
                        nargs='+',
                        help='The lower and upper bounds of the x axis for N_ratio calculation. Only valid when -nr is not specified.')
    parser.add_argument('-nr',
                        '--n_ratio',
                        type=float,
                        nargs='+',
                        help='The x values/centers of the bins (x1, x2) for calculating N_ratio = x1/x2. \
                            If this is not specified, x1=max of x and x2=min of x.')

    args_parse = parser.parse_args()

    return args_parse


def main():

    args = initialize()

    rc('font', **{
        'family': 'sans-serif',
        'sans-serif': ['DejaVu Sans'],
        'size': 10
    })
    # Set the font used for MathJax - more on this later
    rc('mathtext', **{'default': 'regular'})
    plt.rc('font', family='serif')

    plt.figure()  # ready to plot!

    if '*' in args.xvg:
        args.xvg = natsort.natsorted(args.xvg, reverse=False)

    if isinstance(args.xvg, str):  # the case of only one input
        args.xvg = list(args.xvg)
        # for the case of only one input, the legend arugment takes the default
        # but will not be shown
    
    if args.legend is None:
        args.legend = args.xvg

    for i in range(len(args.xvg)):
        result_str = '\nData analysis of the file: %s' % args.xvg[i]
        print(result_str)
        print('=' * (len(result_str) - 1))  # len(result_str) includes \n
        print('Analyzing the file ... ')
        print('Plotting and saving figure ...')

        x, y = [], []
        infile = open('%s' % args.xvg[i], 'r')
        lines = infile.readlines()
        infile.close
        # Parse data
        m = 0
        for line in lines:
            if line[0] == '#' or line[0] == '@':
                m += 1  # number of parameter lines
                if 'xaxis  label "Time (ps)"' in line and args.x_conversion is None:
                    args.x_conversion = 'ps to ns'    

        # read in data starting from (m+1)-th line to the end
        n = m   # line number
        for line in lines[m:-1]:
            n += 1
            if '#' not in line and line[0] != '@':
                # Note that when extending MetaD, COLVAR might append #! FIELDS ... 
                # to an incomplete row of data. Also, when the simulation is extended
                # it might rerun the last portion of the simulation (which might give
                # slightly differen result). We'll just use the results in the extended
                # simulation if this is the case. Note the the quantity of the time frame
                # where the extended simulation starts is should the same as the one of 
                # the same time frame of before the simulation gest extended.
                tokens = line.split()
                x.append(float(tokens[0]))
                y.append(float(tokens[args.column]))
            elif '#' in line:  # the case the MetaD is extended
                tokens = lines[n].split()  # the next line of #! FIELDS ...
                x = np.array(x)
                x = x[x < float(tokens[0])]
                x = list(x)
                y = y[:len(x)]
        x, y = np.array(x), np.array(y)
        
        # Unit conversion
        if args.xlabel is not None:
            if '(' in args.xlabel:
                if '$' in args.xlabel.split('(')[1]:
                    x_unit = args.xlabel.split('$')[1].split('$')[0]
                else:
                    x_unit = args.xlabel.split('(')[1].split(')')[0]
                x_var = args.xlabel.split('(')[0].lower()
                if x_var[-1] == ' ':
                    x_var = x_var.split(' ')[0].lower()
            else:
                x_unit = ''
                x_var = args.xlabel.lower()
        else:
            x_unit = ''
            x_var = None 


        if args.ylabel is not None:
            if '(' in args.ylabel:
                if '$' in args.ylabel.split('(')[1]:
                    y_unit = args.ylabel.split('$')[1].split('$')[0]
                else:
                    y_unit = args.ylabel.split('(')[1].split(')')[0]
                y_var = args.ylabel.split('(')[0].lower()
                if y_var[-1] == ' ':
                    y_var = y_var.split(' ')[0].lower()
            else:
                y_unit = ''
                y_var = args.ylabel.lower()
        else:
            y_unit = ''
            y_var = None

        if args.temp is None:
            args.temp = 298.15
        conversion1 = 1.38064852 * 6.02 * args.temp / 1000  # multiply to convert from kT to kJ/mol
        conversion2 = np.pi/180 # multiply to convert from degree to radian
        conversion3 = 0.239005736  # multiply to convert from kJ/mol to kcal/mol
        
        if args.conversion == 'ps to ns':
            y = y / 1000
            x_unit = ' ns'

        if args.conversion == 'ns to ps':
            y = y * 1000
            y_unit = ' ps'

        if args.conversion == 'kT to kJ/mol':
            y = y * conversion1
            y_unit = ' kcal/mol'
        if args.conversion == 'kJ/mol to kT':
            y = y / conversion1
            y_unit = ' kT'
        if args.conversion == 'kT to kcal/mol':
            y = y * conversion1 * conversion3
            y_unit = ' kcal/mol'
        if args.conversion == 'kcal/mol to kT':
            y = y / (conversion1 * conversion3)
            y_unit = ' kT'
        if args.conversion == 'kJ/mol to kcal/mol':
            y = y * conversion3
            y_unit = 'kcal/mol'
        if args.conversion == 'kcal/mol to kJ/mol':
            y = y / conversion3
            y_unit = 'kJ/mol'
        if args.conversion == 'degree to radian':
            y = y * conversion2
            y_unit = ' radian'
        if args.conversion == 'radian to degree':
            y = y / conversion2
            y_unit = ' degree'

        if args.factor is not None:
            y = y * args.factor

        # Some simple data analysis
        if args.truncate is None:
            # no truncation required
            pass
        else:
            y = y[int(0.01 * float(args.truncate) * len(y)):]  # truncate the first 1% of the data
            x = x[int(0.01 * float(args.truncate) * len(x)):]  
            print('Note that the first %s of the data is truncated, which is the data that the following statistics is based on.' % args.truncate)
        y_avg = np.mean(y)
        y2_avg = np.mean(np.power(y, 2))
        RMSF = np.sqrt((y2_avg - y_avg ** 2)) / y_avg
        print('The average of %s: %5.3f%s (RMSF: %5.3f%s max: %5.3f%s, min: %5.3f%s)' % (y_var, y_avg, y_unit, RMSF, y_unit, np.max(y), y_unit, np.min(y), y_unit))
        if x_unit == ' ns' or x_unit == ' ps':
            y = list(y)
            print('The maximum occurs at %5.4f%s, while the minimum occurs at %5.4f%s.' % (x[y.index(max(y))], x_unit, x[y.index(min(y))], x_unit))
            y = np.array(y)
            diff = np.abs(y - y_avg)
            t_avg = x[np.argmin(diff)]
            print('The configuration at %s%s has the %s (%s%s) that is cloest to the average volume.' % (t_avg, x_unit, y_var, y[np.argmin(diff)], y_unit))

        # Calculate the N_ratio and plot the histogram
        if args.n_ratio is None:   # N_ratio = x(max) / x(min)
            if args.Nr_bound is not None:
                lower_b, upper_b = args.Nr_bound[0], args.Nr_bound[1]
                y = y[y < upper_b]
                y = y[y > lower_b]
            if args.outline is True:
                results = plt.hist(y, bins=args.nbins, edgecolor='black', linewidth=1.2)
            elif args.outline is False:
                results = plt.hist(y, bins=args.nbins)
            N_ratio = np.max(results[0])/np.min(results[0])
        else:
            if args.outline is True:
                results = plt.hist(y, bins=args.nbins, edgecolor='black', linewidth=1.2)
            elif args.outline is False:
                results = plt.hist(y, bins=args.nbins)
            centers = list(results[1])
            for c in args.n_ratio:
                if c not in centers:
                    print('Centers specified for N_ratio calculation not found! Calculation of N_ratio is skipped.')
                    break
            c1, c2 = args.n_ratio[0], args.n_ratio[1]
            N_ratio = results[0][centers.index(c1)] / results[0][centers.index(c2)]
        print(f'N_ratio = {N_ratio: .3f}')

    if args.title is not None:
        plt.title('%s' % args.title)
    plt.xlabel('%s' % args.xlabel)
    #plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    plt.ylabel('%s' % args.ylabel)
    if max(abs(results[0])) >= 10000:
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
    plt.grid(True)

    if args.legend is not None:
        if len(args.xvg) > 1:
            plt.legend(ncol=2)

    plt.savefig('%s.png' % args.pngname)
    plt.show()
