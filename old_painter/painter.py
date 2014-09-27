from PIL import Image, ImageTk
from Tkinter import Tk, Canvas
import numpy as np
import config
from artist import Artist
from utils import chance
from imagetools import ImageTools

targetImage = Image.open(config.TARGET_IMAGE)
precachedTarget = np.array(targetImage, dtype=np.int16).ravel()

class Painter:
	def __init__(self, window):
		self.population = Population()
		self.initWidgets(window)
		
	def initWidgets(self, window):
		self.targetPhoto = ImageTk.PhotoImage(targetImage)
		self.targetCanvas = Canvas(window, width=config.PIC_W, height=config.PIC_W)
		self.targetCanvas.create_image(config.PIC_W/2, config.PIC_H/2, image=self.targetPhoto)
		self.targetCanvas.pack(side='left')
		self.bestCanvas = Canvas(window, width=config.PIC_W, height=config.PIC_H)
		self.bestCanvas.pack(side='left')
		self.currentCanvas = Canvas(window, width=config.PIC_W, height=config.PIC_H)
		self.currentCanvas.pack(side='left')
	
	def update(self):
		if self.population.evolve():
			self.bestImage = ImageTk.PhotoImage(self.population.bestArtist().image)
			self.bestCanvas.create_image(config.PIC_W/2, config.PIC_H/2, image=self.bestImage)
			self.bestCanvas.update_idletasks()
		else:
			self.currentImage = ImageTk.PhotoImage(self.population.artist.image)
			self.currentCanvas.create_image(config.PIC_W/2, config.PIC_H/2, image=self.currentImage)
			self.currentCanvas.update_idletasks()
			self.population.unevolve()

		root.after(0, self.update)

class Population:
	def __init__(self):
		self.artist = Artist(Population.imageFitnessFunction)

	def evolve(self):
		oldFitness = self.artist.fitness
		self.mutationCommands = self.artist.mutate()
		[m.execute() for m in self.mutationCommands]
		if self.artist.fitness > oldFitness:
			return False
		return True

	def unevolve(self):
		if self.mutationCommands:
			[c.undo() for c in self.mutationCommands] 

	def bestArtist(self):
		return self.artist
	
	@staticmethod
	def imageFitnessFunction(image):
		return ImageTools.compareToArray(image, precachedTarget)

root = Tk()
root.geometry(str(config.PIC_W*3)+'x'+str(config.PIC_H))
app = Painter(root)
root.after(0, app.update)
   
if __name__ == '__main__': 
	root.mainloop()


