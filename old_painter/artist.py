from PIL import Image 
from shape import Shape
from utils import chance
from random import randint, choice
import config

class Artist:
	def __init__(self, imageFitnessFunction):
		self.shapes = []
		self.imageFitnessFunction = imageFitnessFunction
		self.rebuild()
		
	class ArtistCommand(object):
		def __init__(self, artist):
			self.artist = artist
			self.didExecute = False

	class AddShapeCommand(ArtistCommand):
		def execute(self):
			numShapes = len(self.artist.shapes)
			if numShapes < config.MAX_SHAPES: 
				index = randint(0, numShapes)
				shape = Shape()
				self.artist.shapes.insert(index, shape)
				self.addedShape = shape 
				self.didExecute = True
		def undo(self):
			if self.didExecute:
				self.artist.shapes.remove(self.addedShape)

	class RemoveShapeCommand(ArtistCommand):
		def execute(self):
			numShapes = len(self.artist.shapes)
			if numShapes > 0:
				self.removedIndex = randint(0, numShapes-1)
				self.removedShape = self.artist.shapes.pop(self.removedIndex)
				self.didExecute = True
		def undo(self):
			if self.didExecute:
				self.artist.shapes.insert(self.removedIndex, self.removedShape)

	class MoveShapeZCommand(ArtistCommand):
		def execute(self):
			numShapes = len(self.artist.shapes)
			if numShapes >= 2:
				self.a = randint(0, numShapes-1)
				while True:
					self.b = randint(0, numShapes-1)
					if self.a != self.b:
						break
				self.swap(self.a, self.b)
				self.didExecute = True
		def undo(self):
			if self.didExecute:
				self.swap(self.a, self.b)
		def swap(self, a, b):
				self.artist.shapes[a], self.artist.shapes[b] = self.artist.shapes[b], self.artist.shapes[a]

	class RebuildCommand(ArtistCommand):
		def execute(self):
			self.oldImage = self.artist.image
			self.oldFitness = self.artist.fitness 
			self.artist.rebuild()
		def undo(self):
			self.artist.image = self.oldImage
			self.artist.fitness = self.oldFitness

	def mutate(self):
		commands = []
		if chance(2):
			r = randint(0, 5)
			if r == 0:
				commands.append(Artist.AddShapeCommand(self))
			elif r == 1:
				commands.append(Artist.RemoveShapeCommand(self))
			elif r == 2:
				commands.append(Artist.RemoveShapeCommand(self))
				commands.append(Artist.AddShapeCommand(self))
			else:
				commands.append(Artist.MoveShapeZCommand(self))
		elif len(self.shapes) > 0:
			shape = choice(self.shapes)
			r = randint(0, 12)
			if r <= 1:
				commands.append(shape.colour.mutate())
			elif r <= 7: 
				commands.extend(shape.mutate(major=True))
			else:
				commands.extend(shape.mutate(major=False))
		commands.append(Artist.RebuildCommand(self))
		return commands
	
	def rebuild(self):
		self.image = self.__buildImage(self.shapes).convert('RGB')
		self.fitness = self.imageFitnessFunction(self.image)
		
	def __buildImage(self, shapes):
		img = Image.new('RGBA', (config.PIC_W, config.PIC_H), 'white')
		for shape in shapes:
			img = Image.alpha_composite(img, shape.image)
		return img

