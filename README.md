PolygonPainter
==============

Inspired by http://rogeralsing.com/2008/12/07/genetic-programming-evolution-of-mona-lisa/

Just learning Python! 

The `old_painter` directory contains an non-breeding strategy in which a single entity or 'artist' is mutated according to a set of weightings, and un-mutated if the fitness is worse than it was before the change. This is similar to the Mona Lisa implementation linked above. We use an object heirarchy of shapes, points, and colours,and use the Command Pattern to encapsulate and optimise changes to these objects. The code is still a mess in places!

I found it to not work as well as I had hoped, and was blindly playing trial and error with the parameters to tweak the quality of the results. The program would quickly reached a local maxima, especially when given full freedom of range on the alpha channel.

For the new version I wanted to use a 'pure' genetic algorithm approach, so each artist is represented by a string of 'DNA', of the format:

    numPolys, polyVertCount, R, G, B, A, x1, y1, x2, y2... R, G, B, A, x1, y1...

We initialise a population and run it through an evolution cycle as follows: 

 - The two fittest pass into the next generation unchanged
 - The rest are bred together in pairs by splicing the DNA sequence to produce an offspring which is then mutated
 - The pairs which are chosen to breed are randomly selected with a bias towards the fittest

That's it! This approach seems to work and it's really hands-off; it just does its thing without any special weightings or guidance. It's also way simpler ;)
 
![Example](http://notes.darkfunction.com/images/ga3.png)


