# adapted from https://github.com/Willfire19/FishToPan/blob/master/fishtopan.py

# Python script to convert FishEye shots to panoramic pictures for 3d use
from PIL import Image
import math
#import sys, getopt

#opts, args = getopt.getopt(argv,

#path = '/Users/gzhou/TL_documents/python/fisheye/'
#filename = "fish-me.jpg"

path = '/Users/gzhou/TL_documents/data/160823-3cam/'
filename = 't2c1.jpg'
#img = Image.open(path, f)
img = Image.open(path+filename)

print(type(img))
img.show()

# assume the src image is square, and its width has even num of pixels
length = img.width / 2
height = img.height
print "Length: " + str(length)
print "Height: " + str(height)

imDest = Image.new("RGB", (4 * length, length) )
# imBilinear = Image.new("RGB", (4 * length, height) )

# backwards
for i in range(0, length):
# for i in range(imDest.height/2, imDest.height):
	for j in range(0, 4*length):

		radius = float(length - i)
		# theta = 2.0 * math.pi * float(4.0 * length - j) / float(4.0 * length)
		theta = 2.0 * math.pi * float(j) / float(4.0 * length)
		# theta = 2.0 * math.pi * float(-j) / float(4.0 * length)

		fTrueX = radius * math.cos(theta)
		fTrueY = radius * math.sin(theta)

		# "normal" mode
		x = int( (round(fTrueX)) + length )
		y = length - int( (round(fTrueY)) )


		# check bounds
		if x >= 0 and x < (2 * length) and y >= 0 and y < (2 * length):
#			if "--flip" in sys.argv:
#				imDest.putpixel( (j, imDest.height - i), img.getpixel( (x, y) ) )
#			else:
				imDest.putpixel( (j, imDest.height-1 - i), img.getpixel( (x, y) ) )
			# imDest.putpixel( (j, imDest.height/2 - i), img.getpixel( (x, y) ) )
			# imDest.putpixel( (j, i), img.getpixel( (x, y) ) )
			# imDest[j, i] = img.getpixel((x, y))

imDest.show()
imDest.save("pan-"+filename, "JPEG")
