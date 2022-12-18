# Day 18 (Boiling Boulders)

## Part 1

We can iterate through all the blocks, and count the number of faces that are
not touching other faces, and add them together. I'm more of less taking the
inverse of the method above, first calculate number of all the faces, and then
remove the faces touching other blocks

## Part 2

[`networkx`][1] comes to rescue! To figure out all the internal faces, I look
at all the air blocks and use networks to see if they can reach the outside by
only going through other airblocks. If not, then remove all the faces touching
the air block because those won't get in contact with water, as water has no
path coming in

[1]: https://networkx.org/
