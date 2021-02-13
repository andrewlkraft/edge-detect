# Edge detect
### Very simple implementations of some image processing algorithms

My inspiration for working on this short project was a [computerphile video](https://www.youtube.com/watch?v=C_zFhWdM4ic&t=0s)

Links to the learning resources and sites I found helfpul are in the code.

Sample flower image from [pexels.com](https://images.pexels.com/photos/736230/pexels-photo-736230.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500). All the rest of the images were taken by me.

I wrote this code for learning purposes, these algorithms are not at all optimized. I wouldn't recommend running them on large images as it could take a while to run (keep it within 1000x1000 pixels).

## sobel.py
Highlights the edges of an image. First it converts the image to greyscale, then blurs slightly to remove noise, then runs sobel operator over the image.
| original | sobel |
|-|-|
| <img src="https://github.com/andrewlkraft/edge-detect/blob/main/images/flower.webp?raw=true" alt="original" width="200" /> | <img src="https://github.com/andrewlkraft/edge-detect/blob/main/images/flower-sobel.webp?raw=true" alt="sobel" width="200" /> |
[src](https://images.pexels.com/photos/736230/pexels-photo-736230.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500)


## kmeans.py
Runs k-means algorithm on an image with specified number k, to find k colors which best represent the image. Then creates a simplified version of the image using those k colors
| original | kmeans (k = 4) |
|-|-|
| <img src="https://github.com/andrewlkraft/edge-detect/blob/main/images/path.jpg?raw=true" alt="original" width="400" /> | <img src="https://github.com/andrewlkraft/edge-detect/blob/main/images/path-kmeans.webp?raw=true" alt="kmeans" width="400" /> |

## cartoon.py
This program uses elements of both the sobel and kmeans programs to produce a cartoon-looking image with thick black lines around the edges of objects
| original | cartoon (k = 8) |
|-|-|
| <img src="https://github.com/andrewlkraft/edge-detect/blob/main/images/clown.jpeg?raw=true" alt="original" width="200" /> | <img src="https://github.com/andrewlkraft/edge-detect/blob/main/images/clown-cartoon.webp?raw=true" alt="cartoon" width="200" /> |

(Yes, that's me in the clown suit)
