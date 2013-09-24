## Procedurally Generating Images in the Style of Piet Mondrian

### Introduction

Piet Mondrian was a Dutch painter. His paintings with orthogonal lines and rectangular splashes of primary colors on white backgrounds are very recognizable.

![](http://media.tumblr.com/tumblr_ltovf9ndAy1qlmzfv.jpg)

I wondered what it would take to programmatically generate Mondrian-esque images. Here's what I came up with.

![](http://media.tumblr.com/tumblr_ltovfuaXsx1qlmzfv.png)

### The Algorithm

The algorithm operates on a two-dimensional grid. Initially, the grid is empty (white or 0) with the perimeter filled in (black or 1) as a sentinel border. The black areas indicate where the lines are to be drawn.

![](http://media.tumblr.com/tumblr_ltovg6qqF51qlmzfv.png)

Next, the algorithm chooses a random number of times to "split" the grid into regions. I choose a random number between 4 and 16 (inclusive) for this.

For each "split" operation, the algorithm randomly chooses to split vertically or horizontally. Depending on the orientation chosen, a random X or a random Y value is chosen as the partition line.

![](http://media.tumblr.com/tumblr_ltovh7xLpb1qlmzfv.png)

The algorithm scans the partition line, looking for existing walls. (Shown in circles.) These existing walls are candidate endpoints for the new line segment. (Initially, only the perimeter border is present, so the first partition will span the entire width or height of the grid.) The algorithm randomly chooses two of the points found and draws a new line between those points.

![](http://media.tumblr.com/tumblr_ltovi15Mrj1qlmzfv.png)

This process repeats until the desired number of split operations have been completed.

![](http://media.tumblr.com/tumblr_ltovivJlr21qlmzfv.png)

Here, three endpoints are available. Two are chosen randomly for the next line.

![](http://media.tumblr.com/tumblr_ltovjtFuIB1qlmzfv.png)

The algorithm keeps track of prior split operations so that no two splits are too close together. (No splits are allowed in the gray region shown in the image. The amount of padding is configurable.)

![](http://media.tumblr.com/tumblr_ltovjzGtUl1qlmzfv.png)

After performing all of the splits, the grid looks something like this.

![](http://media.tumblr.com/tumblr_ltovld6MY71qlmzfv.png)

Next, the algorithm locates all of the distinct regions of the grid using flood fills. The algorithm chooses a random number of regions to "fill" with a color. For each fill, it chooses a random color to use - red, blue or yellow.

![](http://media.tumblr.com/tumblr_ltovlj1Z321qlmzfv.png)

Finally, the perimeter border is chopped off and we have the final result.

![](http://media.tumblr.com/tumblr_ltovmb8xlj1qlmzfv.png)

And that's it - you can have all the procedurally-generated, Mondrian-esque images you want!

### Samples

![](http://media.tumblr.com/tumblr_ltovpxFvz21qlmzfv.png)

![](http://media.tumblr.com/tumblr_ltovq9TfbD1qlmzfv.png)

![](http://media.tumblr.com/tumblr_ltovrasz0N1qlmzfv.png)
