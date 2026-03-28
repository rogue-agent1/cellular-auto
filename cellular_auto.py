#!/usr/bin/env python3
"""Cellular automata — elementary (256 rules) + 2D totalistic."""
import sys

def elementary(rule, width=80, steps=40, init=None):
    table = {tuple(int(b) for b in f"{i:03b}"): (rule>>i)&1 for i in range(8)}
    if init is None: state = [0]*width; state[width//2] = 1
    else: state = init
    rows = [state[:]]
    for _ in range(steps-1):
        new = [table[(state[(i-1)%width], state[i], state[(i+1)%width])] for i in range(width)]
        state = new; rows.append(state[:])
    return rows

def totalistic_2d(width=40, height=40, steps=20, rule="B3/S23"):
    birth = set(); survive = set()
    for part in rule.split("/"):
        if part.startswith("B"): birth = {int(c) for c in part[1:]}
        elif part.startswith("S"): survive = {int(c) for c in part[1:]}
    import random
    grid = [[random.randint(0,1) for _ in range(width)] for _ in range(height)]
    for _ in range(steps):
        new = [[0]*width for _ in range(height)]
        for r in range(height):
            for c in range(width):
                n = sum(grid[(r+dr)%height][(c+dc)%width] for dr in(-1,0,1) for dc in(-1,0,1) if dr or dc)
                if grid[r][c]: new[r][c] = 1 if n in survive else 0
                else: new[r][c] = 1 if n in birth else 0
        grid = new
    return grid

def display_1d(rows):
    for row in rows: print("".join("█" if c else " " for c in row))

def display_2d(grid):
    for row in grid: print("".join("█" if c else "·" for c in row))

def cli():
    if len(sys.argv) < 2:
        print("Usage: cellular_auto <rule_num|2d> [width] [steps]"); sys.exit(1)
    if sys.argv[1] == "2d":
        rule = sys.argv[2] if len(sys.argv)>2 else "B3/S23"
        display_2d(totalistic_2d(rule=rule))
    else:
        rule = int(sys.argv[1])
        w = int(sys.argv[2]) if len(sys.argv)>2 else 80
        s = int(sys.argv[3]) if len(sys.argv)>3 else 40
        print(f"Rule {rule}:"); display_1d(elementary(rule, w, s))

if __name__ == "__main__": cli()
