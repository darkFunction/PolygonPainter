from painter2 import Dna
from PIL import Image, ImageDraw

class ImageTools:
	@staticmethod
	def imageFromDna(dna):
		image = Image.new('RGBA', (Dna.imgSize, Dna.imgSize))
		for i in xrange(dna.genes[0]):
			shape = dna.shapeAtIndex(i)
			ImageDraw.Draw(image).polygon(shape[1], fill=shape[0])
		return image

