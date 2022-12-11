# Day 11 (Monkey in the Middle)

## Part 1

The most annoying part of today's question is probably parsing input. I tried
to do it the more concrete way which took too more time than probably necessary
instead of just `eval`ing the operation :P

## Part 2

As my worry levels no longer get divided, the only operations applied to the
worry levels are modulo operations. The nice thing about modulo operations is
that you can apply a modulo of it's multiple first and it'll get the same
result

E.g., if I want to take modulo 7, I can first take modulo 21 (3x7) first and
get the same result

```text
100 % 7 = 2
100 % 21 = 16 => 16 % 7 = 2
```

21 in this case is also a multiple of 3, so same number can be used to reduce
results modulo 3

```text
100 % 3 = 1
100 % 21 = 16 => 16 % 3 = 1
```

For our monkeys, we just have to find a common multiple for all of their
divisors and use that as our reducer, and always modulo our worry levels with
this number. The most straightforward common multiple is to multiply all the
numbers together, but to optimise it further we can find the
[least common multiple][1] of the monkeys' divisors to make sure we always get
the smallest numbers possible

[1]: https://en.wikipedia.org/wiki/Least_common_multiple
