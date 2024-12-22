from dataclasses import dataclass
from enum import Enum
import queue
import re
import sys

import numpy as np


DEBUG = False


def execute(program, a, b, c):
    output = []
    def combo(operand):
        match operand:
            case 0 | 1 | 2 | 3:
                return operand
            case 4:
                return a
            case 5:
                return b
            case 6:
                return c
            case 7:
                assert False, 'reserved combo operand'

    def dprint(x, *args, **kwargs):
        if DEBUG:
            print(x, *args, **kwargs)

    ptr = 0
    while ptr < len(program):
        opcode = program[ptr]
        operand = program[ptr + 1]
        dprint(f'executing {opcode},{operand}')
        match opcode:
            case 0:  # adv
                num = a
                denom = 1 << combo(operand)
                a = num // denom
                dprint(f'  adv, a = {num} // {denom} = {a}')
            case 1:  # bxl
                dprint(f'  bxl, b = {b} ^ {operand} = {b ^ operand}')
                b = b ^ operand
            case 2:  # bst
                b = combo(operand) % 8
                dprint(f'  bst, b = {combo(operand)} % 8 = {b}')
            case 3:  # jnz
                dprint(f'  jnz, a = {a}')
                if a != 0:
                    dprint(f'    jump to {operand}')
                    ptr = operand
                    continue
            case 4:  # bxc
                dprint(f'  bcx, b = {b} ^ {c} = {b ^ c}')
                b = b ^ c
            case 5:  # out
                dprint(f'  output {combo(operand) % 8}')
                output.append(combo(operand) % 8)
            case 6:  # bdv
                num = a
                denom = 1 << combo(operand)
                b = num // denom
                dprint(f'  bdv, b = {num} // {denom} = {b}')
            case 7:  # cdv
                num = a
                denom = 1 << combo(operand)
                c = num // denom
                dprint(f'  cdv, c = {num} // {denom} = {c}')

        ptr += 2

    return output


def get_next_output(a, test):
    b = a % 8
    if test:
        return b
    b = b ^ 1
    c = a // (1 << b)
    b = b ^ 5
    b = b ^ c
    return b % 8


def find_quine_value(program, test):
    # a has to have some particular value at each step from the back.
    # Find all possible values of those.
    # For each of them, we advance backward.
    candidate_values = [0]
    for rev_step in range(len(program), 0, -1):
        step = rev_step
        new_candidates = []
        for a in candidate_values:
            # We know that executing from step |step| with a = |a| will provide the suffix to the program.
            for pqr in range(8):
                t = 8 * a + pqr
                out = get_next_output(t, test)
                if get_next_output(t, test) == program[step - 1]:
                    new_candidates.append(t)
        candidate_values = new_candidates
        
    return min(candidate_values, default=None)


if __name__ == '__main__':
    filename = sys.argv[1]
    test = 'test' in filename
    lines = [line.strip() for line in open(filename).readlines()]
    a,b,c = [int(line[12:]) for line in lines[:3]]
    program = [int(i) for i in lines[4][9:].split(',')]

    output = ','.join(str(x) for x in execute(program, a, b, c))
    print(f'program output: {output}')

    quine_a = find_quine_value(program, test)
    print(f'quine value for A: {quine_a}')
