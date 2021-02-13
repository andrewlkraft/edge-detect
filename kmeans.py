from PIL import Image
import numpy as np
import sys

rng = np.random.default_rng()

# given a pixel and array of means, output the index of the mean with the closest color to the pixel
def argmindist(pixel, centroids, k):
	d_min, index = np.inf, 0
	for i in range(k):
		dist = 0
		for j in range(3):
			dist += (pixel[j] - centroids[i,j])**2 # no need to take the square root overall, because minimizing x^2 is the same as minimizing |x|
		if dist < d_min:
			d_min = dist
			index = i
	
	return index

# this function will take an array of pixels shape (N, 3) where N = number of pixels
# will output a numpy array shape (k,3) representing the k means and their RGB vals
def kmeans(img_arr, k):
	N, _ = img_arr.shape
	i = 0
	centroids = rng.integers(low=0, high=255, size=(k, 3)) # one array for each RGB value
	while 1:
		i += 1
		print("iteration: %d" % (i))

		new_centroids = np.zeros((k, 3))
		cluster_size = np.zeros(k)	
		for pixel in img_arr:
			index = argmindist(pixel, centroids, k)
			new_centroids[index] += pixel # add the pixel's RGB vals to the new centroids array
			cluster_size[index] += 1
		
		for j in range(k):
			# if there are no nodes in a cluster, reinitialize the cluster to a random node
			if cluster_size[j] == 0:
				new_centroids[j] = rng.integers(low=0,high=255,size=(1,3))
			else:
				for c in range(3):
					new_centroids[j,c] = (new_centroids[j,c] / cluster_size[j]).astype(np.uint8)

		if np.all((centroids-new_centroids)**2 < 32):
			return new_centroids
		centroids = new_centroids


def kmeans_img(img_arr, k):
	# reshape from (X, Y, 3) a 2D array of pixels into (N, 3) a simple array of pixels
	X,Y,_ = img_arr.shape
	img_arr = np.reshape(img_arr, (-1, 3))

	centroids = kmeans(img_arr, k)

	new_img_arr = np.empty(img_arr.shape)
	for i in range(img_arr.shape[0]):
		new_img_arr[i] = centroids[argmindist(img_arr[i], centroids, k)]
	
	new_img = Image.fromarray(np.reshape(new_img_arr, (X,Y,3)).astype(np.uint8))
	return new_img

if __name__ == '__main__':
	try:
		fname = sys.argv[1].split('.')
		k = int(sys.argv[2])
	except(IndexError):
		print("Usage: python kmeans.py <filename> k")
		exit(0)
	
	title = fname[0]

	img = Image.open(sys.argv[1])
	img_arr = np.array(img)

	new_img = kmeans_img(img_arr, k)
	new_img.save(title + "-kmeans.webp")