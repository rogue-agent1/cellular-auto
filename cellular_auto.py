#!/usr/bin/env python3
"""cellular_auto - 1D cellular automata (Wolfram rules)."""
import argparse, sys

def step(cells, rule):
    n = len(cells)
    new = [0] * n
    for i in range(n):
        l = cells[(i-1) % n]
        c = cells[i]
        r = cells[(i+1) % n]
        idx = (l << 2) | (c << 1) | r
        new[i] = (rule >> idx) & 1
    return new

def main():
    p = argparse.ArgumentParser(description="1D cellular automata")
    p.add_argument("rule", type=int, help="Wolfram rule (0-255)")
    p.add_argument("-w","--width", type=int, default=79)
    p.add_argument("-g","--generations", type=int, default=40)
    p.add_argument("--random", action="store_true")
    a = p.parse_args()
    import random
    cells = [0] * a.width
    if a.random:
        cells = [random.randint(0,1) for _ in range(a.width)]
    else:
        cells[a.width // 2] = 1
    print(f"Rule {a.rule}:")
    for _ in range(a.generations):
        print("".join("█" if c else " " for c in cells))
        cells = step(cells, a.rule)

if __name__ == "__main__": main()
