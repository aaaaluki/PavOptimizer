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

This library is inspired in the python [argparse](https://docs.python.org/3/library/argparse.html) module.
