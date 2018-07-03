import argparse

parser = argparse.ArgumentParser()
parser.add_argument('images', help='image path ')
args = parser.parse_args()

print(args.images)
