from dna import Dna
from PIL import Image, ImageDraw
import numpy as np

class ImageTools:
	@staticmethod
	def imageFromDna(dna):
		image = Image.new('RGB', (Dna.imgSize, Dna.imgSize))
		pStart = 4
		pStop = pStart + dna.numSides * 2
		for poly in dna.polyGenerator():
			if poly[3] > 0:
				ImageDraw.Draw(image, 'RGBA').polygon(list(poly[pStart:pStop]), fill=tuple(poly[0:pStart]))
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



