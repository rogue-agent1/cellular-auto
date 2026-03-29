#!/usr/bin/env python3
"""cellular_auto - 1D/2D cellular automata: elementary rules, Game of Life."""
import sys, json

def elementary_ca(rule, width=61, steps=30, init=None):
    if init is None:
        row = [0]*width; row[width//2] = 1
    else:
        row = list(init)
    result = [list(row)]
    for _ in range(steps):
        new_row = [0]*width
        for i in range(width):
            l = row[(i-1)%width]; c = row[i]; r = row[(i+1)%width]
            idx = (l<<2)|(c<<1)|r
            new_row[i] = (rule >> idx) & 1
        row = new_row; result.append(list(row))
    return result

def game_of_life(grid, steps=5):
    rows, cols = len(grid), len(grid[0])
    history = [grid]
    for _ in range(steps):
        new = [[0]*cols for _ in range(rows)]
        for r in range(rows):
            for c in range(cols):
                neighbors = sum(grid[(r+dr)%rows][(c+dc)%cols]
                    for dr in [-1,0,1] for dc in [-1,0,1] if (dr,dc) != (0,0))
                if grid[r][c]:
                    new[r][c] = 1 if neighbors in (2,3) else 0
                else:
                    new[r][c] = 1 if neighbors == 3 else 0
        grid = new; history.append(grid)
    return history

def render_1d(grid):
    for row in grid:
        print("".join("█" if c else " " for c in row))

def count_alive(grid):
    return sum(sum(row) for row in grid)

def main():
    print("Cellular automata demo\n")
    # Rule 30
    ca30 = elementary_ca(30, width=41, steps=20)
    print(f"Rule 30 ({len(ca30)} generations, width {len(ca30[0])}):")
    for row in ca30[:10]:
        print("  " + "".join("█" if c else "·" for c in row))
    # Rule 110 (Turing complete)
    ca110 = elementary_ca(110, width=41, steps=20)
    print(f"\nRule 110 (Turing complete):")
    for row in ca110[:5]:
        print("  " + "".join("█" if c else "·" for c in row))
    # Game of Life - glider
    grid = [[0]*10 for _ in range(10)]
    grid[1][2]=1; grid[2][3]=1; grid[3][1]=1; grid[3][2]=1; grid[3][3]=1
    history = game_of_life(grid, steps=4)
    print(f"\nGame of Life (glider):")
    for i, g in enumerate(history):
        alive = count_alive(g)
        print(f"  Step {i}: {alive} alive")

if __name__ == "__main__":
    main()
