#!/usr/bin/env python3

import os
import sys

def main():
    if len(sys.argv) < 3:
        print(f"usage: {sys.argv[0]} [input.txt] [output.txt]")
        sys.exit()

    try:
        with open(sys.argv[1], "r") as f:
            input_lines = f.readlines()
        with open(sys.argv[2], "r") as f:
            output_lines = f.readlines()
    except IOError as e:
        print(f"Could not read files: {e}")
        sys.exit(e.errno)

    if len(input_lines) != len(output_lines):
        print(f"Number of input lines {len(input_lines)} does not match number of output lines {len(output_lines)}")

    success = 0
    for i in range(len(input_lines)):
        expected_result = sum([int(i) for i in input_lines[i].strip().split()])
        actual_result = int(output_lines[i].strip())
        if expected_result == actual_result:
            success += 1
        else:
            print(f"Line {i} result {actual_result} does not match expected value {expected_result}")

    if success == len(input_lines):
        print("All results matched!")
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
