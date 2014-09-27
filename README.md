PolygonPainter
==============

Inspired by http://rogeralsing.com/2008/12/07/genetic-programming-evolution-of-mona-lisa/

Just learning Python!

The `old_painter` directory contains an non-breeding strategy in which a single entity or 'artist' is mutated according to a set of weightings, and un-mutated if the fitness is worse than it was before the change. This is similar to the Mona Lisa implementation, however I didn't spend long playing with the weightings and found it to not work as well as I hoped, especially when given full freedom of range with the alpha channel. It uses the Command Pattern to encapsulate and optimise mutations. The code is a bit of a mess in places.

For the new version I wanted to use a more traditional genetic algorithm approach, so each artist is represented by a string of 'DNA', of the format:

    numPolys, polyVertCount, R, G, B, A, x1, y1, x2, y2... R, G, B, A, x1, y1...

We initialise a population and run it through an evolution as follows: 

 - The two fittest pass into the next generation unchanged
 - The rest are bred together by splicing the DNA sequence to produce an offspring which is then mutated
 - The artists which are chosen to breed are randomly selected with a bias towards the fittest

![Example](http://notes.darkfunction.com/images/tux.png)
