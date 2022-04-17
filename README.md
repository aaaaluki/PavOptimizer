# PAV Optimization Library

This library was created for finding the parameters that maximizes a program/script.

It works as follows:
1. For each argument get N samples linearly spaced between the given range.
2. Try all the combination of these samples and find the max value.
3. Make the range smaller and repeat from step one.

This *might* not be the best solution for finding the max value, but works (it's
just really slow).

**IMPORTANT**: The evaluation program / script must **ONLY** output to `stdout`
the value to maximize as decimal number, i.e.: '12.34'.

Simple usage:
```python
    optimizer = pav_optimizer.PavOptimizer('optimize.sh')
    optimizer.add_argument('-m', (0, 1))
    optimizer.add_argument('-n', (0, 1))

    optimizer.run()
```

Sample output:
```
Iteration 1/1
Progress |##                              | 6.25% [0 / 1]s	Current Max value: 79.00 % -> -m: 0.0000, -n: 0.0000
Progress |####                            | 12.50% [1 / 10]s	Current Max value: 82.65 % -> -m: 0.0000, -n: 0.3333
Progress |######                          | 18.75% [2 / 13]s	Current Max value: 86.32 % -> -m: 0.0000, -n: 0.6667
Progress |##########                      | 31.25% [5 / 13]s	Current Max value: 90.74 % -> -m: 0.3333, -n: 0.0000
Progress |############                    | 37.50% [7 / 12]s	Current Max value: 90.83 % -> -m: 0.3333, -n: 0.3333
Progress |##############                  | 43.75% [8 / 11]s	Current Max value: 90.91 % -> -m: 0.3333, -n: 0.6667
Progress |################################| 100.00% [23 / 0]s
Max value: 90.9100 % -> -m: 0.3333, -n: 0.6667
	-m Range 0.0000 - 0.6667
	-n Range 0.3333 - 1.0000
```

This library is inspired in the python [argparse](https://docs.python.org/3/library/argparse.html) module.
