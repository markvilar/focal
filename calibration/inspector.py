import cv2
import os
import sys

class StereoInspector(object):
	def __init__(self, root: str, fps: int=30):
		assert root[-1] == "/", "Invalid root directory extension."
		assert os.path.exists(root), "Root directory does not exist."
		assert fps > 0, "FPS must be positive and non-zero."

		self.root = root
		self.left_directory = root + "left_unrectified"
		self.right_directory = root + "right_unrectified"
		self.fps = fps

	def get_image_files(self, directory: str):
		files = [os.path.join(directory, f) for f 
			in os.listdir(directory)
			if os.path.isfile(os.path.join(directory, f))]
		files = [f for f in files if os.path.splitext(f)[-1] == ".png"]
		return files
		
	def inspect(self):
		left_files = self.get_image_files(self.left_directory)
		right_files = self.get_image_files(self.right_directory)

		left_files.sort()
		right_files.sort()

		indices_file = open(self.root + "indices.txt", "w")
		
		for index, (left_file, right_file) in \
			enumerate(zip(left_files, right_files)):

			left_image = cv2.imread(left_file)
			right_image = cv2.imread(right_file)

			cv2.imshow("Left", left_image)
			cv2.imshow("Right", right_image)

			key_code = cv2.waitKey(int(1000/self.fps))

			if key_code == 32:
				sys.stdout.write("Collected index: {0}\n"
					.format(index))
				sys.stdout.flush()
				indices_file.write("{0}\n".format(index))
			elif key_code == 27:
				break
			elif key_code == -1:
				continue

		cv2.destroyAllWindows()
		indices_file.close()
