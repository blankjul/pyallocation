import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('metamodel', metavar='model', type=str,
                    help='The metamodel to be used.')

parser.add_argument('fname', metavar='fname', type=str,
                    help='The file for the output.')

args = parser.parse_args()
print(args.accumulate(args.integers))