from imagetools import ImageTools 
from dna import Dna
from random import triangular, randint

class Population:
	def __init__(self, size, polyCount, vertexCount, targetImage):
		self.size = size
		self.targetImage = targetImage
		self.artists = [Dna(polyCount, vertexCount) for i in xrange(size)]
		[a.randomisePolys() for a in self.artists]
		self.cycles = 0
		self.improvements = 0
		self.mutationLevel = 0

	def luckyIndex(self):
		bottom = self.size / 5, 							# knock off the bottom 
		return int(triangular(0, self.size - bottom, 0)) 	# bias towards better fitness with triangle random tending to 0

	def evolve(self):
		self.lastBest = self.bestArtist()
		self.newArtists = self.artists[:2] 			# top two always make it
		while len(self.newArtists) < self.size:
			child = self.artists[self.luckyIndex()].splice(self.artists[self.luckyIndex()])
			child.mutate(self.mutationLevel)
			self.newArtists.append(child)
		self.artists = self.newArtists
		self.sortByFitness()
		self.cycles += 1
		if self.cycles % 100 == 0:
			self.mutationLevel = self.mutationLevel + 1 if self.mutationLevel < 2 else 0
			print "Switched to mutation level:", self.mutationLevel
		if self.lastBest != self.bestArtist():
			self.improvements += 1
			return True
		return False

	def sortByFitness(self):
		self.artists.sort(key=lambda dna: self.calcFitness(dna))
	
	def bestArtist(self):
		return self.artists[0]
		
	def calcFitness(self, dna):
		image = ImageTools.imageFromDna(dna)
		fitness = ImageTools.compare(image, self.targetImage)
		return fitness
		

