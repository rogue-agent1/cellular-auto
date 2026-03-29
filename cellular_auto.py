#!/usr/bin/env python3
"""cellular_auto - 1D cellular automaton (all 256 Wolfram rules)."""
import argparse

def step(cells, rule):
    n = len(cells); new = [0]*n
    for i in range(n):
        left = cells[(i-1) % n]; center = cells[i]; right = cells[(i+1) % n]
        idx = (left << 2) | (center << 1) | right
        new[i] = (rule >> idx) & 1
    return new

def main():
    p = argparse.ArgumentParser(description="1D cellular automaton")
    p.add_argument("-r", "--rule", type=int, default=110)
    p.add_argument("-w", "--width", type=int, default=79)
    p.add_argument("-g", "--generations", type=int, default=40)
    p.add_argument("--random", action="store_true")
    args = p.parse_args()
    import random
    if args.random:
        cells = [random.randint(0,1) for _ in range(args.width)]
    else:
        cells = [0]*args.width; cells[args.width//2] = 1
    print(f"Rule {args.rule} ({args.rule:08b})")
    for _ in range(args.generations):
        print("".join("█" if c else " " for c in cells))
        cells = step(cells, args.rule)

if __name__ == "__main__":
    main()
