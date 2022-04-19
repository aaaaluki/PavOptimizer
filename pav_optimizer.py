# Author: luki

"""PAV Optimization Library

This library was created for finding the parameters that maximize a program / script.
It works as follows:
    1. For each argument get N samples linearly spaced between the given range.
    2. Try all the combination of these samples and find the max value.
    3. Make the range smaller and repeat from step one.

This might not be the best solution for finding the max value, but works (it's
just really slow).

IMPORTANT: The evaluation program / script must ONLY output to stdout the value
           to maximize as decimal number, i.e.: '12.34'.

Simple usage:
    optimizer = pav_optimizer.PavOptimizer('optimize.sh')
    optimizer.add_argument('-m', (0, 1))
    optimizer.add_argument('-n', (0, 1))
    optimizer.run()

This library is inspired in the python argparse module.
"""

import datetime
import itertools
import os.path
import subprocess
import time
from collections import defaultdict
from typing import Dict, List, Tuple

import numpy as np
from progress.bar import Bar

# This is the minimum value of samples needed for the script to work
DEFAULT_SAMPLE_NUM = 4


class _PavError(Exception):
    pass


class _PavArgument:
    def __init__(self, name: str, value: float) -> None:
        self.m_name = name
        self.m_value = value


class PavOptimizer:
    def __init__(self, cmd: str, iteration_num: int = 1, sample_num: int = DEFAULT_SAMPLE_NUM) -> None:
        if not os.path.isfile(cmd):
            raise _PavError('File "{}" does not exist'.format(cmd))

        self.m_cmd = cmd
        self.m_iteration_num = iteration_num
        self.m_sample_num = max(sample_num, DEFAULT_SAMPLE_NUM)
        self.m_arguments = {}
        self.m_exec_time = None

    def set_exec_time(self, t_exec: float) -> None:
        self.m_exec_time = t_exec

    def add_argument(self, name: str, start_range: Tuple[float, float]) -> None:
        if name in self.m_arguments.keys():
            raise _PavError('Argument "{}" already added'.format(name))

        if len(start_range) != 2:
            raise _PavError('Invalid start range: start and end values are needed')

        if start_range[0] > start_range[1]:
            raise _PavError('Invalid start range: the first value should be smaller than the second one')

        self.m_arguments[name] = np.linspace(start_range[0], start_range[1], num=self.m_sample_num)

    def run(self) -> None:
        start_time = time.time()

        if self.m_iteration_num > 0 and self.m_exec_time is not None:
            time_estimation = self.m_exec_time * self.m_iteration_num * self.m_sample_num ** len(self.m_arguments)
            print('Time estimation: {}'.format(str(datetime.timedelta(seconds=time_estimation))))
        elif self.m_iteration_num < 0:
            print('Running until the heat death of the universe ...')

        i = 0
        while True:
            if i == self.m_iteration_num:
                break

            iteration_str = 'Iteration {}'.format(i + 1)
            if self.m_iteration_num > 0:
                iteration_str += '/{}'.format(self.m_iteration_num)
            print(iteration_str)
            i += 1

            args_range = self.__find_maximum(self.m_arguments)

            for name, arg_range in args_range.items():
                self.m_arguments[name] = np.linspace(arg_range[0], arg_range[1], num=self.m_sample_num)

        print('Execution time: {}'.format(str(datetime.timedelta(seconds=time.time() - start_time))))

    def __function(self, args: List[_PavArgument]) -> float:
        cmd = [self.m_cmd]
        for arg in args:
            cmd += [arg.m_name, str(arg.m_value)]

        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, error = proc.communicate()

        if error:
            print('[ERROR]: {}'.format(error.decode().strip()))
            exit(1)

        return float(out.decode().strip())

    def __find_maximum(self, args: Dict[str, np.ndarray]) -> Dict[str, Tuple[float, float]]:
        # Vars for finding max
        indices = defaultdict()
        val_max = 0

        arg_values = []
        for name, values in args.items():
            arg_values.append([_PavArgument(name, v) for v in values])

        bar = Bar('Progress', fill='#', suffix='%(percent).2f%% [%(elapsed)d / %(eta)d]s',
                  max=self.m_sample_num ** len(self.m_arguments))

        # Sauce: https://stackoverflow.com/a/3034027/13313449
        for combination in itertools.product(*arg_values):
            # This should be at the end, but if this is printed first the
            # output is nicer. Although the time estimation is a little buggy.
            bar.next()

            result = None
            while result is None:
                result = self.__function(combination)

            if result > val_max:
                val_max = result
                max_status = "\t Current Max value: {:.2f} % ->".format(val_max)
                for arg in combination:
                    indices[arg.m_name] = np.where(args[arg.m_name] == arg.m_value)[0][0]
                    max_status += ' {}: {:.4f},'.format(arg.m_name, arg.m_value)

                # Print all unless last comma
                print(max_status[:-1])

        bar.finish()

        # Print max value with optimal argument values and new ranges
        result_str = 'Max value: {:.4f} % ->'.format(val_max)
        args_range = dict()
        for name, values in args.items():
            idx = indices[name]
            args_range[name] = (values[max(idx - 1, 0)],
                                values[min(idx + 1, self.m_sample_num - 1)])
            result_str += ' {}: {:.4f},'.format(name, values[idx])

        # Remove last comma
        result_str = result_str[:-1]

        for name, arg_range in args_range.items():
            result_str += '\n\t{} Range {:.4f} - {:.4f}'.format(name, arg_range[0], arg_range[1])

        print(result_str + '\n')

        return args_range
