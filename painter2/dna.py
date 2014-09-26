''' 
Array format:
numPolys, numSides, r, g, b, a, x1, y1, x2, y2... r, g, b, a, x1, y1... 
'''

import numpy
from random import randint

class Dna:
	imgSize = 0
	def __init__(self, numPolys, numSides):
		self.headerSize = 2
		self.polyDataLen = 4 + numSides * 2
		self.length = self.headerSize + (numPolys * self.polyDataLen) 
		self.genes = numpy.zeros(self.length, dtype=numpy.int)
		self.genes[0], self.genes[1] = numPolys, numSides

	def mutate(self):
		index = randint(self.headerSize, self.length-1)
		if self.indexIsColour(index):
			self.genes[index] = randint(0, 255)
		else:
			self.genes[index] = randint(0, Dna.imgSize)
				
	def indexIsColour(self, index):
		return (index - self.headerSize) % self.polyDataLen < 4

	def shapeAtIndex(self, index):
		offset = self.headerSize + (index * self.polyDataLen)
		colour = tuple(self.genes[offset:offset+4])
		coords = zip(self.genes[offset+4 : offset+self.polyDataLen : 2], self.genes[offset+5 : offset+self.polyDataLen : 2])
		return (colour, coords) 

	def splice(self, dna):
		assert dna.genes[0] == self.genes[0]
		assert dna.genes[1] == self.genes[1]
		child = Dna(dna.genes[0], dna.genes[1])
		for i in xrange(2, self.length):
			if randint(0, 1) == 0:
				numpy.append(child.genes, self.genes[i])
			else:
				numpy.append(child.genes, dna.genes[i])
		return child

