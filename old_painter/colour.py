from random import randint, choice
from utils import chance
import config

class Colour:
	def __init__(self):
		self.initChannels()

	def initChannels(self):
		self.r, self.g, self.b, self.a = randint(0, 255), randint(0, 255), randint(0, 255), randint(config.TRANSPARENCY_MIN, config.TRANSPARENCY_MAX)

	class ColourCommand(object):
		def __init__(self, colour):
			self.colour = colour

	class ChangeColourCommand(ColourCommand):
		def execute(self):
			self.oldValues = self.colour.getTuple()
			if chance(2):
				self.colour.initChannels()
			else:
				r = randint(0,4)
				if r == 0: 
					self.colour.r = randint(0, 255)
				elif r == 1: 
					self.colour.g = randint(0, 255)
				elif r == 2:
					self.colour.b = randint(0, 255)
				elif r == 3:
					self.colour.a = randint(config.TRANSPARENCY_MIN, config.TRANSPARENCY_MAX)

		def undo(self):
			(self.colour.r, self.colour.g, self.colour.b, self.colour.a) = self.oldValues

	def mutate(self):
		command = Colour.ChangeColourCommand(self)
		return command 

	def getTuple(self):
		return (self.r, self.g, self.b, self.a)


