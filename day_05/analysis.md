# Day 05 (Supply Stacks)

## Part 1

Seems like a fun scenario, why not simulate it? I went down the OOP path to
make it slightly clearer how each object behave, and the implementation should
be straightforward. The data parsing, however, is not. A regex and some
calculated indices are used to grab the data

## Part 2

I actually didn't read the questions clearly and implemented this first, only
to realize that the crates are stacked in reverse order and therefore needs to
reverse the stacked list. I can just remove the removal from the first solution
