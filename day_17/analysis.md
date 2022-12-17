# Day 17 (Pyroclastic Flow)

## Part 1

This part can be emulated directly as the problem described. The implementation
is slightly complicated, but go through the movements and collision detections
step-by-step and it should be straightforward!

## Part 2

We really can't simulate 1 trillion (or billion for [long scale][1] people)
actions in reasonable time<sup>*[citation needed]*</sup>, so we need to find
the pattern. After careful educated guessing (by which I mean I just looked at
part 1's output and hoped that it would generalize), I decided a cycle should
start before 500 rocks are settled. After that, if the first kind of rock
`####` is created on the same action while the top 11 layers of settled rocks
are the same, we can quite confidently say that a cycle has been detected. Get
the cycle count, and run the remainder the same way as part 1

[1]: https://en.wikipedia.org/wiki/Long_and_short_scales#Long_scale
