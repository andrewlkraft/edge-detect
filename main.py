from PIL import Image
import numpy as np
import sys

# creates greyscale version of given image
# inputs: np.array of shape (x,y,3) representing an RGB image of dimensions (x,y)
# outputs: np.array of shape (x,y) representing the greyscale version of that image
#
# luminosity coefficients from https://en.wikipedia.org/wiki/Relative_luminance
RED, GRN, BLU = 0.2126, 0.7152, 0.0722
def create_greyscale(img_array):
	dims = img_array.shape
	greyscale_array = np.empty(dims[:2])
	for x in range(dims[0]):
		for y in range(dims[1]):
			greyscale_array[x,y] = RED*img_array[x,y,0] + GRN*img_array[x,y,1]  + BLU*img_array[x,y,2]
	return greyscale_array

# creates gaussian kernal with specified dimensions
# inputs: 
# d representing side length of square kernal matrix
# sigma representing standard deviation for gaussian distribution
# outputs: np.array of shape (2r-1, 2r-1) representing gaussian kernal
# 
# https://en.wikipedia.org/wiki/Gaussian_blur
def gauss_kernal(d, sigma):
	if(d % 2 == 0):
		print("d must be odd")
		exit(0)

	k = 1/(2*sigma**2)
	A = k/np.pi	
	r = np.floor(d/2)

	out = np.empty((d, d))

	for x in range(d):
		for y in range(d):
			out[x,y] = A*np.exp(-k*((x-r)**2+(y-r)**2))

	return out

#
# creates blurred version of given image (so far only works for greyscale images)
# inputs: np.array of shape (x,y) representing an image of dimensions (x,y)
# outputs: np.array of shape (x,y) representing blurred version of image
#
# einsum: https://stackoverflow.com/questions/26089893/understanding-numpys-einsum
def gaussian_blur(img_array):
	dims = img_array.shape
	output_array = np.empty(dims)

	kernal = gauss_kernal(5, 1)

	for x in range(dims[0]):
		for y in range(dims[1]):
			xmin, ymin = max(0, x-2), max(0, y-2)
			xmax, ymax = min(dims[0], x+3), min(dims[1], y+3)
			avg = np.einsum('ij,ij->', img_array[xmin:xmax, ymin:ymax], kernal[xmin-x+2:xmax-x+2, ymin-y+2:ymax-y+2])
			avg /= np.einsum('ij->', kernal[xmin-x+2:xmax-x+2,ymin-y+2:ymax-y+2])

			output_array[x,y] = avg
	
	return output_array


# inputs: greyscale gaussian blurred image in the form of a numpy array (x,y)
# outputs: edges of the image in numpy array (x,y)
def sobel_edge_detect(img_array):
	dims = img_array.shape
	output_array = np.empty(dims)

	kernal = np.array([[-1,0,1], [-2,0,2], [-1,0,1]])

	for x in range(dims[0]):
		for y in range(dims[1]):
			xmin, ymin = max(0, x-1), max(0, y-1)
			xmax, ymax = min(dims[0], x+2), min(dims[1], y+2)
			x_grad = np.einsum('ij,ij->', img_array[xmin:xmax,ymin:ymax], kernal[xmin-x+1:xmax-x+1, ymin-y+1:ymax-y+1])
			y_grad = np.einsum('ij,ji->', img_array[xmin:xmax,ymin:ymax], kernal[ymin-y+1:ymax-y+1, xmin-x+1:xmax-x+1])

			output_array[x,y] = np.sqrt(x_grad**2 + y_grad**2)
	
	return output_array


if __name__ == "__main__":
	# first we open the image and convert it into a numpy array of pixel values.

	try:	
		fname = sys.argv[1].split('.')
	except(IndexError):
		print("Usage: python main.py <filename>")
		exit(0)

	title = fname[0]
	ext = fname[1]

	img = Image.open(title + '.' + ext)
	img_arr = np.array(img)

	print("Converting to greyscale...")
	greyscale_arr = create_greyscale(img_arr)
	greyscale_img = Image.fromarray(greyscale_arr)
	greyscale_img.save(title +'-gs.'+ ext)

	print("Blurring...")
	greyscale_blur_arr = gaussian_blur(greyscale_arr)
	greyscale_blur_img = Image.fromarray(greyscale_blur_arr)
	greyscale_blur_img.save(title +'-gs-blur.'+ ext)

	print("Detecting edges...")
	edge_arr = sobel_edge_detect(greyscale_blur_arr)
	edge_img = Image.fromarray(edge_arr)
	edge_img.save(title + '-edge.' + ext)
