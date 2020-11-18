import cv2

class ExtrinsicCalibrator(object):
	def __init__(self, root):
		self.root = root
		raise NotImplementedError

	def calibrate(self):
		raise NotImplementedError
