# Day 09 (Rope Bridge)

## Part 1 & 2

I love to use complex numbers to represent 2D coordinates due to their ease in
calculations. I esentially hard-coded all possible scenarios:

* If previous segment is 0 or 1 steps away (including diagonal), then next
  segment doesn't move
* If previous segment is 2 steps away (including diagonal), then the next
  segment moves based on previous segment's direction
* If previous segment is 3 or more steps away, then something is wrong
