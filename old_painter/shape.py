from PIL import Image, ImageDraw
from random import randint
from colour import Colour
from utils import chance
import config

class Shape:
	def __init__(self):
		self.poly = self.__randPoly(randint(config.POLY_MIN_SIDES, config.POLY_MAX_SIDES), 0, 0, config.PIC_W, config.PIC_H)
		self.colour = Colour() 
		self.image = self.buildImage()

	class ShapeCommand(object):
		def __init__(self, shape):
			self.shape = shape;
			self.didExecute = False

	class InsertPointCommand(ShapeCommand):
		def execute(self):
			if len(self.shape.poly) < config.POLY_MAX_SIDES:
				index = randint(1, len(self.shape.poly)-2)
				prevPoint = self.shape.poly[index-1]
				nextPoint = self.shape.poly[index+1]
				newPoint = (((prevPoint[0] + nextPoint[0]) / 2), ((prevPoint[1] + nextPoint[1]) / 2))
				self.shape.poly.insert(index, newPoint)
				self.insertedPoint = newPoint
				self.didExecute = True
		def undo(self):
			if self.didExecute:
				self.shape.poly.remove(self.insertedPoint)
	
	class RemovePointCommand(ShapeCommand):
		def execute(self):
			if len(self.shape.poly) > config.POLY_MIN_SIDES:
				self.poppedIndex = randint(0, len(self.shape.poly)-1)
				self.poppedPoint = self.shape.poly.pop(self.poppedIndex)
				self.didExecute = True
		def undo(self):
			if self.didExecute:
				self.shape.poly.insert(self.poppedIndex, self.poppedPoint) 

	class MovePointCommand(ShapeCommand):
		def __init__(self, shape, isMajor):
			super(Shape.MovePointCommand, self).__init__(shape)
			self.isMajor = isMajor
		def execute(self):
			if self.isMajor:
				move = config.PIC_W / 3
			else:
				move = 3
			self.index = randint(0, len(self.shape.poly)-1)
			point = self.shape.poly[self.index]
			x, y = point[0], point[1]
			self.oldPoint = point 
			x += randint(-move, move)
			x = min(config.PIC_W, max(0, x))
			y += randint(-move, move)
			y = min(config.PIC_H, max(0, y))
			self.shape.poly[self.index] = (x, y) 
		def undo(self):
			self.shape.poly[self.index] = self.oldPoint

	class RebuildCommand(ShapeCommand):
		def execute(self):
			self.oldImage = self.shape.image
			self.shape.image = self.shape.buildImage()
		def undo(self):
			self.shape.image = self.oldImage
	
	def mutate(self, major=False):
		commands = []
		if chance(10):
			if chance(1):
				commands.append(Shape.RemovePointCommand(self))
			else:
				commands.append(Shape.InsertPointCommand(self))
		else:
			commands.append(Shape.MovePointCommand(self, isMajor=major))
		commands.append(Shape.RebuildCommand(self))
		return commands

	def buildImage(self):
		image = Image.new('RGBA', (config.PIC_W, config.PIC_H))
		ImageDraw.Draw(image).polygon(self.poly, fill=self.colour.getTuple())
		return image

	def __randPoly(self, sides, minX, minY, maxX, maxY):
		zoneDivisor = randint(1, 4)
		zone = (randint(0, zoneDivisor-1), randint(0, zoneDivisor-1))
		size = ((maxX - minX) / zoneDivisor, (maxY - minY) / zoneDivisor)
		points = []
		start = (zone[0] * size[0], zone[1] * size[1])
		for i in xrange(sides):
			points.append((randint(start[0], start[0] + size[0]), randint(start[1], start[1] + size[1])))
		return points
	
