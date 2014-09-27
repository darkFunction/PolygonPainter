from dna import Dna
from imagetools import ImageTools
from PIL import Image, ImageTk
from population import Population
from Tkinter import Tk, Canvas

IMG_SIZE = 256
POPULATION_SIZE = 10
VERTEX_COUNT = 6
Dna.imgSize = IMG_SIZE
targetImage = Image.open('../image.png')

class Painter:
	def __init__(self, window):
		self.population = Population(POPULATION_SIZE, VERTEX_COUNT, targetImage)
		self.targetPhoto = ImageTk.PhotoImage(targetImage)
		self.initWidgets(window)
		
	def initWidgets(self, window):
		self.targetCanvas = Canvas(window, width=IMG_SIZE, height=IMG_SIZE)
		self.targetCanvas.create_image(IMG_SIZE/2, IMG_SIZE/2, image=self.targetPhoto)
		self.targetCanvas.pack(side='left')
		self.bestCanvas = Canvas(window, width=IMG_SIZE, height=IMG_SIZE)
		self.bestCanvas.pack(side='left')
	
	def update(self):
		self.population.evolve()
		image = ImageTools.imageFromDna(self.population.artists[0])
		self.bestImage = ImageTk.PhotoImage(ImageTools.imageFromDna(self.population.artists[0]))
		self.bestCanvas.create_image(IMG_SIZE/2, IMG_SIZE/2, image=self.bestImage)
		self.bestCanvas.update_idletasks()
		root.after(0, self.update)

root = Tk()
root.title("PolyPainter")
root.geometry(str(IMG_SIZE*2)+'x'+str(IMG_SIZE))
app = Painter(root)
root.after(0, app.update)
   
if __name__ == '__main__': 
	root.mainloop()

