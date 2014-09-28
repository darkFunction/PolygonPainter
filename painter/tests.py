from dna import Dna
from imagetools import ImageTools

def testDnaSize():
	dna = Dna(1, 3)
	assert len(dna.genes) == 12
	assert len(dna.genes) == dna.length
	dna2 = Dna(2, 3)
	assert dna2.length == 22
	dna3 = Dna(2, 4)
	assert dna3.length == 26

def testDnaInit():
	dna = Dna(3, 4)
	assert dna.genes[0] == 3
	assert dna.genes[1] == 4
	for i in range(2, dna.length-1):
		assert dna.genes[i] == 0

def testIndexCategorisation():
	dna = Dna(1, 3)
	for i in xrange(2, 5):
		assert dna.indexIsColour(i) == True 
	for i in xrange(6, 12):
		assert dna.indexIsColour(i) == False

def testMutationRanges():
	dna = Dna(1, 3)
	for i in xrange(100):
		dna.mutate(1)
	for i in xrange(dna.headerSize, dna.length):
		gene = dna.genes[i]
		if dna.indexIsColour(i):
			assert gene > 0 and gene <= 255
		else:
			assert gene > 0 and gene <= Dna.imgSize

def testShapeExtraction():
	dna = Dna(2, 3)
	dna.genes = [2, 3, 
					255, 0, 0, 255,
					1, 2, 3, 4, 5, 6, 
					255, 0, 0, 255,
					7, 8, 9, 10, 11, 12]
	assert sorted(dna.polyAtIndex(1)) == sorted([(255, 0, 0, 255), [(7, 8), (9, 10), (11, 12)]])

def testImageCreation():
	dna = Dna(2, 3)
	dna.genes = [2, 3, 
					255, 0, 0, 100,
					10, 10, 250, 250, 10, 250,
					0, 255, 0, 50,
					10, 10, 250, 10, 10, 250]	
	image = ImageTools.imageFromDna(dna)	
	image.show()

def testDnaSpliceValidLength():
	mother = Dna(3, 3)
	father = Dna(3, 3)
	child = mother.splice(father)
	assert len(child.genes) == len(mother.genes)

def testDnaPolySwap():
	dna = Dna(2, 3)
	dna.genes =      [2, 3, 255, 0, 0, 100, 1, 2, 3, 4, 5, 6, 0, 255, 0, 50, 7, 8, 9, 10, 11, 12]	
	expectedResult = [2, 3, 0, 255, 0, 50, 7, 8, 9, 10, 11, 12, 255, 0, 0, 100, 1, 2, 3, 4, 5, 6]
	dna.swapPolys(0, 1)
	assert not cmp(dna.genes, expectedResult)

Dna.imgSize = 256
testDnaSize()
testDnaInit()
testIndexCategorisation()
testMutationRanges()
testShapeExtraction()
testImageCreation()
testDnaSpliceValidLength()
testDnaPolySwap()
print "Tests passed"
