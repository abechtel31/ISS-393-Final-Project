#!/usr/bin/env Python
# -*- coding: utf-8 -*-

### Names: Abby Bechtel, Nic Cordova, Nate Everett, Suleiman Karkoutli, Matthew Parnham
# IDs: 2312284, 2302109, 2296318, 2275013
# Emails: abechtel@chapman.edu, cordova@chapman.edu, everett@chapman.edu, karko101@chapman.edu, parnham@chapman.edu
# Course: CPSC393 Interterm 2020
# Assignment: Final

# Sources: PyImageSearch https://www.pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/
###

"""
This program module uses the face_recognition package to encode the faces from passangers of the International Space Station.

This module is first trained on a set of labeled (known) faces from the dataset

Usage:

Run the command: python encode_faces.py --dataset dataset --encodings encodings.pickle
"""

from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os

# Reads an image in from given command line arg
def readImage(im):
	# load the input image and convert it from BGR to RGB
	image = cv2.imread(im)

	if image is None: #the image file could not be loaded
		raise TypeError

	r = 1000.0 / image.shape[1]
	dim = (1000, int(image.shape[0] * r))

	# perform the actual resizing of the image
	image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
	return image


def main():
	# parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--dataset", required=True,
		help="path to input directory of faces + images")
	ap.add_argument("-e", "--encodings", required=True,
		help="path to serialized db of facial encodings")
	ap.add_argument("-d", "--detection-method", type=str, default="cnn",
		help="face detection model to use: either `hog` or `cnn`")
	args = vars(ap.parse_args())

	# grab the paths to the input images in our dataset
	print("[INFO] quantifying faces...")
	imagePaths = list(paths.list_images(args["dataset"]))

	# initialize the list of known encodings and known names
	knownEncodings = []
	knownNames = []

	# loop over the image paths
	for (i, imagePath) in enumerate(imagePaths):
		# extract the person name from the image path
		print("[INFO] processing image {}/{}".format(i + 1,
			len(imagePaths)))
		name = imagePath.split(os.path.sep)[-2]

		# read and resize the input image and convert from OpenCV color ordering to dlib ordering (RGB)
		try:
			image = readImage(imagePath)

		except TypeError:
			print("The file image file was not properly loaded")

		rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

		# detect the (x, y)-coordinates of the bounding boxes
		# corresponding to each face in the input image
		boxes = face_recognition.face_locations(rgb,
			model=args["detection_method"])

		# compute the facial embedding for the face
		encodings = face_recognition.face_encodings(rgb, boxes, num_jitters = 10)

		# loop over the encodings
		for encoding in encodings:
			# add each encoding + name to our set of known names and
			# encodings
			knownEncodings.append(encoding)
			knownNames.append(name)

	# dump the facial encodings + names to disk
	print("[INFO] serializing encodings...")
	data = {"encodings": knownEncodings, "names": knownNames}
	f = open(args["encodings"], "wb")
	f.write(pickle.dumps(data))
	f.close()

if __name__ == "__main__":
	main()
