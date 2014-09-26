from dna import Dna
from imagetools import ImageTools
from PIL import Image
from population import Population

Dna.imgSize = 256
targetImage = Image.open('../image.png')
population = Population(100, targetImage)
for i in xrange(10):
	population.evolve()

