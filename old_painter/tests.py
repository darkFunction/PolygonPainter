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

	runArtistTests()
	   
if __name__ == '__main__': 
	runTests()


