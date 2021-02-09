from PIL import Image
import numpy as np
import sys




if __name__ == '__main__':
	try:
		fname = argv[1].split('.')
		k = argv[2]
	except(IndexError):
		print("Usage: python kmeans.py <filename> <means>")
		exit(0)
	
	title = fname[0]