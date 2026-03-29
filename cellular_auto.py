#!/usr/bin/env python3
"""Cellular automata: 1D elementary, Game of Life, Langton's Ant, wireworld."""
import sys, random, time

def elementary(rule=110, width=80, steps=40, init=None):
    if init is None:
        state = [0]*width; state[width//2] = 1
    else: state = init
    for _ in range(steps):
        print("".join("█" if c else " " for c in state))
        new = [0]*width
        for i in range(width):
            l = state[(i-1)%width]; c = state[i]; r = state[(i+1)%width]
            idx = (l<<2)|(c<<1)|r
            new[i] = (rule >> idx) & 1
        state = new

def game_of_life(w=60, h=30, steps=50, density=0.3):
    grid = [[1 if random.random() < density else 0 for _ in range(w)] for _ in range(h)]
    for step in range(steps):
        print(f"\033[H\033[J=== Game of Life (step {step}) ===")
        for row in grid: print("".join("█" if c else " " for c in row))
        new = [[0]*w for _ in range(h)]
        for y in range(h):
            for x in range(w):
                n = sum(grid[(y+dy)%h][(x+dx)%w] for dy in (-1,0,1) for dx in (-1,0,1)) - grid[y][x]
                if grid[y][x]: new[y][x] = 1 if n in (2,3) else 0
                else: new[y][x] = 1 if n == 3 else 0
        grid = new; time.sleep(0.1)

def langton_ant(w=60, h=30, steps=500):
    grid = [[0]*w for _ in range(h)]; x, y, d = w//2, h//2, 0
    dirs = [(0,-1),(1,0),(0,1),(-1,0)]
    for _ in range(steps):
        if grid[y][x] == 0: d = (d+1)%4; grid[y][x] = 1
        else: d = (d-1)%4; grid[y][x] = 0
        x = (x+dirs[d][0])%w; y = (y+dirs[d][1])%h
    for row in grid: print("".join("█" if c else "·" for c in row))

def main():
    import argparse
    p = argparse.ArgumentParser(description="Cellular automata")
    p.add_argument("type", nargs="?", default="elementary", choices=["elementary","life","ant"])
    p.add_argument("-r", "--rule", type=int, default=110)
    p.add_argument("-s", "--steps", type=int, default=40)
    args = p.parse_args()
    random.seed(42)
    if args.type == "elementary":
        print(f"Rule {args.rule}:"); elementary(args.rule, steps=args.steps)
    elif args.type == "life": game_of_life(steps=args.steps)
    elif args.type == "ant": langton_ant(steps=args.steps*10)

if __name__ == "__main__": main()
