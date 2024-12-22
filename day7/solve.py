import sys

import numpy as np

lines = open(sys.argv[1]).readlines()

def calibrate(lines, operators):
    calibration_result = 0
    for line in lines:
        tokens = line.split()
        res = int(tokens[0].strip(':'))
        operands = [int(t) for t in tokens[1:]]
        stack = [operands[0]]
        for y in operands[1:]:
            new_stack = []
            for x in stack:
                for op in operators:
                    new_stack.append(op(x,y))
            stack = new_stack
        if res in stack:
            calibration_result += res
    return calibration_result


add = lambda x, y: x + y
mul = lambda x, y: x * y
cat = lambda x, y: int(str(x) + str(y))

print(calibrate(lines, [add, mul]))
print(calibrate(lines, [add, mul, cat]))
