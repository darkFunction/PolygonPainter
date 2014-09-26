from dna import Dna
from PIL import Image, ImageDraw
import numpy as np

class ImageTools:
	@staticmethod
	def imageFromDna(dna):
		image = Image.new('RGB', (Dna.imgSize, Dna.imgSize))
		for i in xrange(0, dna.genes[0]):
			shape = dna.shapeAtIndex(i)
			ImageDraw.Draw(image, 'RGBA').polygon(shape[1], fill=shape[0])
		return image
	
	@staticmethod
	def compareToArray(image, array):
		imageArray = np.array(image, dtype=np.int16).ravel()
		diffArray = np.subtract(imageArray, array)
		#return np.sum((imageArray-array)**2)
		return np.sum(np.abs(diffArray))

	@staticmethod
	def compare(image1, image2):
		array1 = np.array(image1, dtype=np.int16).ravel()
		array2 = np.array(image2, dtype=np.int16).ravel()
		diffArray = np.subtract(array1, array2)
		return np.sum(np.abs(diffArray))



