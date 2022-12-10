# Day 10 (Cathode-Ray Tube)

## Part 1

The data output logic is implemented such that it'll yield the cycle and
register values every time the cycle number is incremented

```py
def run_program(self, program: list[str]) -> _BasicGenerator[tuple[_Cycle, _X]]:
    """"""
    for line in program:
        match line.split():
            case ["noop"]:
                yield self._inc_cycle()
            case ["addx", value_str]:
                value = int(value_str)
                for _ in range(2):
                    yield self._inc_cycle()
                self.x += value
            case _:
                raise ValueError(f"Unknown command {line}")

def _inc_cycle(self) -> tuple[_Cycle, _X]:
    """"""
    self.cycle += 1
    return self.cycle, self.x
```

The generator saves memory and slightly easier to write (no need to initiate
and append to a list and return at the end), and the result can be further
filtered in `sum`

## Part 2

The output values are mapped to the 2D screen via `divmod`. Don't forget to
convert 1-based cycle number to 0-based CRT column number
