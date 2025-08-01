#! /usr/bin/env python
#
# author: Kyle A. Damm
# date:   29-07-2025
#

import numpy as np
import re

def extract_au_array(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if line.startswith("active"):
            print(line)
        if line.startswith("step= 1"):
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()

                # Remove all leading "Au[" prefixes
                while next_line.startswith("Au["):
                    next_line = next_line[3:].strip()

                # Remove all trailing brackets (assuming each "Au[" adds one closing "]")
                next_line = next_line.rstrip("] ").strip()
                print(next_line)
                # Use regex to extract all numbers, including negative and floating-point values
                numbers = [float(num) for num in re.findall(r"[-+]?\d*\.\d+(?:[eE][-+]?\d+)?", next_line)]

                return np.array(numbers)

            break  # Only process the first match

    return None

if __name__=='__main__':

    # read in files
    cpu_array = extract_au_array("cpu.dat")
    gpu_array = extract_au_array("gpu.dat")

    # evaluate the L2 error norm
    diff = np.abs(cpu_array-gpu_array)
    L2_error = np.sqrt(np.dot(diff,diff))
    print("L2 error norm: ", L2_error)
