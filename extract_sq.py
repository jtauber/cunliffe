#!/usr/bin/env python3

with open("out2.txt") as f:
    state = 1
    for line in f:
        line = line.strip().lstrip("†*")
        if line:
            if state == 1:
                if "]" in line:
                    print(line.split("]")[0] + "]")
            state = 2
        else:
            state = 1
