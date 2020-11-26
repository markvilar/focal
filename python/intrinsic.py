import cv2
import glob 
import numpy as np
import os

from typing import Tuple

class IntrinsicCalibrator(object):
	def __init__(self, directory: str, pattern_size: Tuple[int, int],
		tile_size: float):
		assert directory[-1] == '/', \
			"Directory path must end with '/'."
		assert os.path.exists(directory), \
			"Invalid data directory."
		assert pattern_size[0] > 0 and pattern_size[1] > 0, \
			"Pattern size must be larger than zero."
		assert tile_size > 0, "Tile size must be larger than zero."

		self.directory = directory
		self.pattern_size = pattern_size
		self.tile_size = tile_size

		self.object_points = np.zeros(
			(pattern_size[0], pattern_size[1], 3), np.float32)

		# 5x8x3
		print(self.object_points.shape) 
		# 2x3x7
		print(np.mgrid[0:pattern_size[0], 0:pattern_size[1]][0])
		print(np.mgrid[0:pattern_size[0], 0:pattern_size[1]][1])
			
		self.object_points[:, :, 0] = \
			np.mgrid[0:pattern_size[0], 0:pattern_size[1]][0] \
			* tile_size

		print(self.object_points)
			#np.mgrid[0:pattern_size[0], 0:pattern_size[1]] \
			#.T.reshape(-1, 1) * tile_size

		print(self.object_points.shape)

		self.criteria = (cv2.TERM_CRITERIA_EPS 
			+ cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
		self.camera_model = None

	def get_image_files(self):
		image_files = [f for f in os.listdir(self.directory)
			if os.path.isfile(os.path.join(self.directory, f))]
		image_files = [os.path.join(self.directory, f) 
			for f in image_files]
		image_files = [f for f in image_files 
			if os.path.splitext(f)[-1] == ".png"]
		
		image_files.sort()
		return image_files

	def show_images(self):
		image_files = self.get_image_files()

		for image_file in image_files:
			image = cv2.imread(image_file)
			
			cv2.imshow("Image", image)
			key_code = cv2.waitKey(33)

			if key_code == 27:
				break
			elif key_code == -1:
				continue

	def calibrate(self):
		img_files = self.get_image_files()
		
		n_found = 0
		for img_file in img_files:
			img = cv2.imread(img_file)

			# Downscale image.
			width = int(0.5 * img.shape[1])
			height = int(0.5 * img.shape[0])
			img = cv2.resize(img, (width, height))
			
			# Create grayscale.
			gray_img= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

			# Create constant limit adaptive histogram equalization.
			clahe = cv2.createCLAHE(clipLimit=5.0, 
				tileGridSize=(8, 8))

			#filtered_img = clahe.apply(gray_img)
			filtered_img = gray_img

			cv2.imshow("Filtered", filtered_img)
			cv2.waitKey(10)
			ret, corners = cv2.findChessboardCorners(filtered_img,
				self.pattern_size, 
				cv2.CALIB_CB_ADAPTIVE_THRESH)
				#+ cv2.CALIB_CB_FAST_CHECK \
				#+ cv2.CALIB_CB_NORMALIZE_IMAGE)
			if ret:
				n_found = n_found + 1
				for corner in corners:
					x, y = corner.ravel()
					cv2.imshow("Grayscale", gray_img)
					cv2.circle(gray_img, (x,y), 3, 
						(0,0,255), -1)
		print(n_found)
