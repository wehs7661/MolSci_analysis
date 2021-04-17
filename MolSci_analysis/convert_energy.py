import argparse

def initialize():
    parser = argparse.ArgumentParser(
        description='This is a simple calculator convert kT to kcal/mol.')
    parser.add_argument('-T',
                        '--temp',
                        type=float,
                        help='Temperature of interest.')
    parser.add_argument('-f',
                        '--factor',
                        type=float,
                        default=1.0,
                        help='The factor to be multiplied to the answer.')
    args_parse = parser.parse_args()

    return args_parse

def main():
    args = initialize()
    k = 1.38064852E-23  # Boltzmann constant
    N_A = 6.02214086E23 # Avogadro constant
    print((k * args.temp) * N_A / 1000 * args.factor)
            






