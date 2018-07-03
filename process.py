import argparse
import time

time.sleep(1)


parser = argparse.ArgumentParser()
parser.add_argument('images', help='image path ')
args = parser.parse_args()

print(args.images)
