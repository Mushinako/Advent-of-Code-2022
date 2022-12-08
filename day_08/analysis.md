# Day 08 (Treetop Tree House)

## Part 1

Given I'm too lazy to figure out the number of trees on the side, I decided to
just count the number of trees that can't be seen from the outside and subtract
that from the total number of trees

For each direction, if the maximum height of the trees in that direction is
less then the current tree height, then this tree can be seen from that
direction and we can skip this tree

## Part 2

The prompt stated that the at least one of the viewing distance for trees on
the edge would be 0, signaling that their scenic score would be 0, so we only
need to consider the inner trees again

Same as part 1, we calculate the score in 4 directions. The tricky part is
about left (negative column) and top (negative row) sides because those tree
orders need to be reversed to check the trees closest to the reference tree
first
