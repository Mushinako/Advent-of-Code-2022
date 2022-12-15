# Day 15 (Beacon Exclusion Zone)

## Part 1

A simple set keeps tracks of all the positions that can't host beacons, and is
populated by iterating through the rules. The length of the set is the result!

## Part 2

I tried the brute force ways:

1. Make a 4M * 4M map/set that keeps track of all the positions that can't host
   beacons; constrained by memory
2. Do the same as [Part 1](#part-1) but for 4M times; takes too long

Actually, we can kinda do the 2nd way, but we need to drastically increase it's
speed. One idea is that instead of keeping track of the individual cells, we
keep track of the ranges. Sure, the logic for reducing and combining ranges are
rather complicated, but it's still much faster than going through the 4M cells
on each direction, as there're fewer than 30 sensors
