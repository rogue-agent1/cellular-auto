#!/usr/bin/env python3
"""cellular_auto - Elementary CA, Game of Life, Langton's Ant."""
import sys, argparse

def elementary_ca(rule, width=80, steps=40, init=None):
    if init is None:
        state = [0]*width; state[width//2] = 1
    else: state = list(init)
    lines = []
    for _ in range(steps):
        lines.append("".join("█" if c else " " for c in state))
        new = [0]*width
        for i in range(width):
            l = state[(i-1)%width]; c = state[i]; r = state[(i+1)%width]
            idx = (l<<2)|(c<<1)|r
            new[i] = (rule >> idx) & 1
        state = new
    return lines

def game_of_life(grid, steps=10):
    rows, cols = len(grid), len(grid[0])
    frames = []
    for _ in range(steps):
        frames.append(["".join("█" if c else "·" for c in row) for row in grid])
        new = [[0]*cols for _ in range(rows)]
        for r in range(rows):
            for c in range(cols):
                n = sum(grid[(r+dr)%rows][(c+dc)%cols] for dr in (-1,0,1) for dc in (-1,0,1) if dr or dc)
                if grid[r][c]: new[r][c] = 1 if n in (2,3) else 0
                else: new[r][c] = 1 if n == 3 else 0
        grid = new
    return frames

def langtons_ant(width=80, height=40, steps=500):
    grid = [[0]*width for _ in range(height)]
    x, y, d = width//2, height//2, 0
    dx = [0,1,0,-1]; dy = [-1,0,1,0]
    path = [(x,y)]
    for _ in range(steps):
        if grid[y][x] == 0: d = (d+1)%4
        else: d = (d-1)%4
        grid[y][x] ^= 1
        x = (x+dx[d])%width; y = (y+dy[d])%height
        path.append((x,y))
    return grid, path

def main():
    p = argparse.ArgumentParser(description="Cellular automata")
    sub = p.add_subparsers(dest="cmd")
    e = sub.add_parser("elementary"); e.add_argument("-r","--rule",type=int,default=110)
    e.add_argument("-w","--width",type=int,default=80); e.add_argument("-s","--steps",type=int,default=40)
    g = sub.add_parser("life"); g.add_argument("-s","--steps",type=int,default=10)
    g.add_argument("--pattern",default="glider",choices=["glider","blinker","rpentomino"])
    a = sub.add_parser("ant"); a.add_argument("-s","--steps",type=int,default=500)
    sub.add_parser("demo")
    args = p.parse_args()
    if args.cmd == "elementary":
        for line in elementary_ca(args.rule, args.width, args.steps): print(line)
    elif args.cmd == "life":
        grid = [[0]*20 for _ in range(20)]
        if args.pattern == "glider":
            for r,c in [(0,1),(1,2),(2,0),(2,1),(2,2)]: grid[r+5][c+5] = 1
        elif args.pattern == "blinker":
            for c in range(3): grid[10][9+c] = 1
        elif args.pattern == "rpentomino":
            for r,c in [(0,1),(0,2),(1,0),(1,1),(2,1)]: grid[r+9][c+9] = 1
        for i, frame in enumerate(game_of_life(grid, args.steps)):
            if i == 0 or i == args.steps-1:
                print(f"--- Step {i} ---")
                for row in frame: print(row)
    elif args.cmd == "ant":
        grid, path = langtons_ant(steps=args.steps)
        filled = sum(sum(row) for row in grid)
        print(f"After {args.steps} steps: {filled} filled cells, ant at {path[-1]}")
    elif args.cmd == "demo":
        print("=== Rule 110 ===")
        for line in elementary_ca(110, 60, 20): print(line)
    else: p.print_help()

if __name__ == "__main__":
    main()
