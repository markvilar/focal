import cv2
import glob 
import numpy as np
import os

class IntrinsicCalibrator(object):
	def __init__(self, root, indices):
		# Sanity check.
		assert os.path.exists(root), "Invalid root directory."
		assert len(indices) > 0, "Invalid image indices."
		assert not any(indices) < 0, "Invalid image indices."

		self.root = root
		self.indices = indices
		self.criteria = (cv2.TERM_CRITERIA_EPS 
			+ cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
		self.camera_model = None

	def load_images(self):
		image_files = [f for f in os.listdir(self.root)
			if os.path.isfile(os.path.join(self.root, f))]
		image_files = [os.path.join(self.root, f) for f in image_files]
		image_files = [f for f in image_files 
			if os.path.splitext(f)[-1] == ".png"]
		
		image_files.sort()

		for image_file in image_files:
			image = cv2.imread(image_file)
			grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

			cv2.imshow("Image", image)
			key_code = cv2.waitKey(33)

			if key_code == 27:
				break
			elif key_code == -1:
				continue

	def calibrate(self):
		raise NotImplementedError
