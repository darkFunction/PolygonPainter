from dna import Dna
from imagetools import ImageTools
from PIL import Image, ImageTk
from population import Population
from Tkinter import Tk, Canvas
from settings import Settings

SIZE = Settings.imageSize

Dna.imgSize = SIZE
targetImage = Image.open(Settings.targetImageName)

class Painter:
	def __init__(self, window):
		self.population = Population(Settings.populationSize, Settings.polyCount, Settings.vertexCount, targetImage)
		self.targetPhoto = ImageTk.PhotoImage(targetImage)
		self.initWidgets(window)
		
	def initWidgets(self, window):
		self.targetCanvas = Canvas(window, width=SIZE, height=SIZE)
		self.targetCanvas.create_image(SIZE/2, SIZE/2, image=self.targetPhoto)
		self.targetCanvas.pack(side='left')
		self.bestCanvas = Canvas(window, width=SIZE, height=SIZE)
		self.bestCanvas.pack(side='left')
	
	def update(self):
		if self.population.evolve():
			print "Cycles", self.population.cycles
			print "Improvements", self.population.improvements
			image = ImageTools.imageFromDna(self.population.artists[0])
			self.bestImage = ImageTk.PhotoImage(ImageTools.imageFromDna(self.population.artists[0]))
			self.bestCanvas.create_image(SIZE/2, SIZE/2, image=self.bestImage)
			self.bestCanvas.update_idletasks()
		root.after(0, self.update)

root = Tk()
root.title("PolyPainter")
root.geometry(str(SIZE*2)+'x'+str(SIZE))
app = Painter(root)
root.after(0, app.update)
   
if __name__ == '__main__': 
	root.mainloop()

