import sys
import cv2
import numpy as np
import argparse
import matplotlib.pyplot as plt 
from matplotlib import rc 

def initialize():
    parser = argparse.ArgumentParser(
        description='This code plots the angle and dihedral angle distribution for the modified System 2.')
    parser.add_argument('-f',
                        '--figs',
                        nargs='+',
                        help='The number of figures to be combined.')
    parser.add_argument('-d',
                        '--dimension',
                        type=int,
                        nargs='+',
                        help='The dimension of the subplots (n_cols, n_rows).')
    parser.add_argument('-s',
                        '--size',
                        type=int,
                        nargs='+',
                        help='The dimensions of the figure (length, width).')
    parser.add_argument('-t',
                        '--titles',
                        nargs='+',
                        help='The title of each subplot.')
    parser.add_argument('-b',
                        '--border',
                        default=False,
                        action='store_true',
                        help='Whether to show the border lines of each subplot.')
    parser.add_argument('-n',
                        '--pngname',
                        help='The name of the figure, not cluding the extension.')

    args_parse = parser.parse_args()

    return args_parse

def get_fig_dimension(n_subplots):
    """
    Gets the dimension of the figure given the number of subplots. The figure
    will be as close as to a square as possible.

    Parameters
    ----------
    n_subplots (int): The number of subplots.

    Returns
    -------
    n_rows (int): The number of rows in the figure.
    n_cols (int): The number of columns in the figure.
    """
    if int(np.sqrt(n_subplots) + 0.5) ** 2 == n_subplots:
        # perfect square number
        n_cols = int(np.sqrt(n_subplots))
    else:
        n_cols = int(np.floor(np.sqrt(n_subplots))) + 1 
    
    if n_subplots % n_cols == 0:
        n_rows = int(n_subplots / n_cols)
    else:
        n_rows = int(np.floor(n_subplots / n_cols)) + 1 
    
    return n_cols, n_rows

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

    if args.size is None:
        fig = plt.figure()
    else:
        if len(args.size) != 2:
            print('Warning: wrong number of arguments for specifying the figure size.')
        else:
            fig = plt.figure(figsize=tuple(args.size))

    if args.dimension is None:
        n_cols, n_rows = get_fig_dimension(len(args.figs))
    else:
        if len(args.dimension) != 2:
            print('Warning: wrong number of arguments for specifying the dimension of the subplots.')
        else:
            n_cols = args.dimension[0]
            n_rows = args.dimension[1]

    if args.titles is not None:
        if len(args.figs) != len(args.titles):
            print('Error: The number of titles does not match the number of subplots.')
            sys.exit()

    for i in range(len(args.figs)):
        image = cv2.imread(args.figs[i], cv2.IMREAD_COLOR)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        fig.add_subplot(n_rows, n_cols, i + 1)
        plt.imshow(image_rgb)
        if args.border is True:
            plt.xticks([])
            plt.yticks([])
        elif args.border is False:
            plt.axis('off')  
        if args.titles is not None:
            plt.title(args.titles[i])
        
    plt.tight_layout(rect=[0, 0, 1, 1])
    plt.savefig(f'{args.pngname}.png', dpi=600)
        

