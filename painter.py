from random import randint, choice
from PIL import Image, ImageDraw
from copy import deepcopy
from Tkinter import Tk, Canvas
from PIL import Image, ImageDraw, ImageTk
import numpy as np

PIC_W, PIC_H = 256, 256 
TARGET_IMAGE = 'image2.png'
MAX_SHAPES = 50
POLY_MIN_SIDES = 3
POLY_MAX_SIDES = 6
TRANSPARENCY_MIN = 10
TRANSPARENCY_MAX = 60

targetImage = Image.open(TARGET_IMAGE)
precachedTarget = np.array(targetImage, dtype=np.int16).ravel()

class Painter:
    def __init__(self, window):
        self.population = Population()
        self.initWidgets(window)
        
    def initWidgets(self, window):
        self.targetPhoto = ImageTk.PhotoImage(targetImage)
        self.targetCanvas = Canvas(window, width=PIC_W, height=PIC_W)
        self.targetCanvas.create_image(PIC_W/2, PIC_H/2, image=self.targetPhoto)
        self.targetCanvas.pack(side='left')
        self.bestCanvas = Canvas(window, width=PIC_W, height=PIC_H)
        self.bestCanvas.pack(side='left')
    
    def update(self):
        self.population.evolve()
        image = ImageTk.PhotoImage(self.population.bestArtist().image)
        self.bestCanvas.create_image(PIC_W/2, PIC_H/2, image=image)
        self.bestCanvas.update_idletasks()
        root.after(0, self.update)


def chance(i):
    return randint(0, i) == 1

class ImageTools:
    @staticmethod
    def compareToTarget(image1):
        array1 = np.array(image1, dtype=np.int16).ravel()
        diffArray = np.subtract(array1, precachedTarget)
        #return np.sum((array1-precachedTarget)**2)
        return np.sum(np.abs(diffArray))

    @staticmethod
    def compare(image1, image2):
        array1 = np.array(image1, dtype=np.int16).ravel()
        array2 = np.array(image2, dtype=np.int16).ravel()
        diffArray = np.subtract(array1, array2)
        return np.sum(np.abs(diffArray))


class Population:
    def __init__(self):
        self.artist = Artist()

    def evolve(self):
        oldFitness = self.artist.fitness
        mutationCommands = self.artist.mutate()
        [m.execute() for m in mutationCommands]
        if self.artist.fitness > oldFitness:
            [c.undo() for c in mutationCommands] 

    def bestArtist(self):
        return self.artist

class Artist:
    def __init__(self):
        self.shapes = []
        self.rebuild()
        
    def getFitness(self):
        return ImageTools.compareToTarget(self.image)

    class ArtistCommand(object):
        def __init__(self, artist):
            self.artist = artist
            self.didExecute = False

    class AddShapeCommand(ArtistCommand):
        def execute(self):
            numShapes = len(self.artist.shapes)
            if numShapes < MAX_SHAPES: 
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
        r = randint(0, 12)
        if r == 0:
            r2 = randint(0, 5)
            if r2 == 0:
                commands.append(Artist.AddShapeCommand(self))
            elif r2 == 1:
                commands.append(Artist.RemoveShapeCommand(self))
            elif r2 == 2:
                commands.append(Artist.RemoveShapeCommand(self))
                commands.append(Artist.AddShapeCommand(self))
            else:
                commands.append(Artist.MoveShapeZCommand(self))
        elif len(self.shapes) > 0:
            shape = choice(self.shapes)
            if r <= 3:
                commands.append(shape.colour.mutate())
            elif r <= 8: 
                commands.extend(shape.mutate(major=True))
            else:
                commands.extend(shape.mutate(major=False))
        commands.append(Artist.RebuildCommand(self))
        return commands
        
    def rebuild(self):
        self.image = self.__buildImage(self.shapes).convert('RGB')
        self.fitness = self.getFitness()

    def __buildImage(self, shapes):
        img = Image.new('RGBA', (PIC_W, PIC_H), 'white')
        for shape in shapes:
            img = Image.alpha_composite(img, shape.image)
        return img
        
class Shape:
    def __init__(self):
        self.poly = self.__randPoly(randint(POLY_MIN_SIDES, POLY_MAX_SIDES), PIC_W, PIC_H)
        self.colour = Colour() 
        self.image = self.buildImage()

    class ShapeCommand(object):
        def __init__(self, shape):
            self.shape = shape;
            self.didExecute = False

    class InsertPointCommand(ShapeCommand):
        def execute(self):
            if len(self.shape.poly) < POLY_MAX_SIDES:
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
            if len(self.shape.poly) > POLY_MIN_SIDES:
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
                move = PIC_W / 3
            else:
                move = 3
            self.index = randint(0, len(self.shape.poly)-1)
            point = self.shape.poly[self.index]
            x, y = point[0], point[1]
            self.oldPoint = (x, y)
            x += randint(-move, move)
            x = min(PIC_W, max(0, x))
            y += randint(-move, move)
            y = min(PIC_H, max(0, y))
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
        image = Image.new('RGBA', (PIC_W, PIC_H))
        ImageDraw.Draw(image).polygon(self.poly, fill=self.colour.getTuple())
        return image

    def __randPoly(self, sides, maxX, maxY):
        points = []
        for i in xrange(sides):
            points.append((randint(0, maxX), randint(0, maxY)))
        return points
    
class Colour:
    def __init__(self):
        self.initChannels()

    def initChannels(self):
        self.r, self.g, self.b, self.a = randint(0, 255), randint(0, 255), randint(0, 255), randint(TRANSPARENCY_MIN, TRANSPARENCY_MAX)

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
                    self.colour.a = randint(TRANSPARENCY_MIN, TRANSPARENCY_MAX)

        def undo(self):
            (self.colour.r, self.colour.g, self.colour.b, self.colour.a) = self.oldValues

    def mutate(self):
        command = Colour.ChangeColourCommand(self)
        return command 

    def getTuple(self):
        return (self.r, self.g, self.b, self.a)

def runTests():

    def runArtistTests():
        artist = Artist()
    
        def setup():
            for i in xrange(5):
                Artist.AddShapeCommand(artist).execute()
            artist.rebuild()
   
        ''' Ensure the command sequence modifies the artist image then
            restores to previous state when undo is invoked '''
        def testCommandsWork(commands):
            image = artist.image
            [c.execute() for c in commands]
            artist.rebuild()
            assert ImageTools.compare(image, artist.image) != 0
            [c.undo() for c in commands]
            artist.rebuild()
            assert ImageTools.compare(image, artist.image) == 0
        
        setup()
        testCommandsWork([Artist.AddShapeCommand(artist)])
        testCommandsWork([Artist.RemoveShapeCommand(artist)])
        testCommandsWork([Artist.MoveShapeZCommand(artist)])

        shape = artist.shapes[0]
        shapeRebuildCommand = Shape.RebuildCommand(shape)
        testCommandsWork([Shape.MovePointCommand(shape, True), shapeRebuildCommand])
        testCommandsWork([Shape.MovePointCommand(shape, False), shapeRebuildCommand])
        #testCommandsWork([Shape.RemovePointCommand(shape), shapeRebuildCommand])

    runArtistTests()
       
#runTests()

root = Tk()
root.geometry(str(PIC_W*2)+'x'+str(PIC_H))
app = Painter(root)
root.after(0, app.update)
   
if __name__ == '__main__': 
    root.mainloop()


