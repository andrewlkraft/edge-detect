# python libs
from PIL import Image
import numpy as np
import sys

# local libs
from sobel import create_greyscale, sobel_edge_detect, gaussian_blur
from kmeans import kmeans_img

THRESHOLD = 50

def draw_edges(img_arr, edge_arr):
	X,Y,_ = img_arr.shape
	img_pixels = np.reshape(img_arr, (-1,3))
	edge_pixels = np.reshape(edge_arr, (-1))
	N = len(edge_pixels)
	for i in range(N):
		if edge_pixels[i] > THRESHOLD:
			img_pixels[i] = np.zeros((1,3))
	
	output = np.reshape(img_pixels, (X,Y,3))
	return output

if __name__ == "__main__":
	# first we open the image and convert it into a numpy array of pixel values.

	try:	
		fname = sys.argv[1].split('.')
		k = int(sys.argv[2])
	except(IndexError):
		print("Usage: python cartoon.py <filename> <number of colors to use>")
		exit(0)

	try:
		flag = sys.argv[3]
	except(IndexError):
		flag = ""

	title = fname[0]

	img = Image.open(sys.argv[1])
	img_arr = np.array(img)

	print("Converting to greyscale...")
	greyscale_arr = create_greyscale(img_arr)
	greyscale_img = Image.fromarray(greyscale_arr)
	greyscale_img.save(title +'-gs.webp')

	print("Blurring...")
	greyscale_blur_arr = gaussian_blur(greyscale_arr, 5, 8)
	greyscale_blur_img = Image.fromarray(greyscale_blur_arr)
	greyscale_blur_img.save(title +'-gs-blur.webp')

	print("Running sobel...")
	edge_arr, angles = sobel_edge_detect(greyscale_blur_arr)
	edge_img = Image.fromarray(edge_arr)
	edge_img.save(title + '-sobel.webp')

	print("Finding kmeans...")
	# if flag=="--blur":
		# print("Blurring...")
		# blur_arr = blur(img_arr, 5, 8)
		# blur_img = Image.fromarray(blur_arr)
		# blur_img.save(title +'-blur.webp')
	kmeans_img = kmeans_img(img_arr, k)
	kmeans_img.save(title + '-kmeans.webp')
	kmeans_arr = np.array(kmeans_img)

	print("Drawing cartoon...")
	cartoon_arr = draw_edges(kmeans_arr, edge_arr)
	cartoon_img = Image.fromarray(cartoon_arr)
	cartoon_img.save(title + '-cartoon.webp')