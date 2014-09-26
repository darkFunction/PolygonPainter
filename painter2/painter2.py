from dna import Dna
from imagetools import ImageTools
from PIL import Image
from population import Population

Dna.imgSize = 256
targetImage = Image.open('../image.png')
population = Population(50, targetImage)
for i in xrange(1000):
	population.evolve()
image = ImageTools.imageFromDna(population.artists[0])
image.show()

