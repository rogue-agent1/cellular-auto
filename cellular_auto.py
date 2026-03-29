#!/usr/bin/env python3
"""Elementary cellular automata (1D) and Game of Life (2D)."""
import sys

def elementary_ca(rule, width=61, steps=30):
    row = [0]*width; row[width//2] = 1
    rows = [row[:]]
    for _ in range(steps):
        new = [0]*width
        for i in range(1, width-1):
            pattern = (row[i-1]<<2) | (row[i]<<1) | row[i+1]
            new[i] = (rule >> pattern) & 1
        row = new; rows.append(row[:])
    return rows

def game_of_life(grid, steps=5):
    h, w = len(grid), len(grid[0]); frames = [grid]
    for _ in range(steps):
        new = [[0]*w for _ in range(h)]
        for y in range(h):
            for x in range(w):
                n = sum(grid[(y+dy)%h][(x+dx)%w] for dy in (-1,0,1) for dx in (-1,0,1) if (dy,dx)!=(0,0))
                if grid[y][x]: new[y][x] = 1 if n in (2,3) else 0
                else: new[y][x] = 1 if n == 3 else 0
        grid = new; frames.append(grid)
    return frames

def main():
    rows = elementary_ca(110, 41, 20)
    print("Rule 110:")
    for row in rows: print("".join("█" if c else " " for c in row))
    glider = [[0]*10 for _ in range(10)]
    glider[1][2]=glider[2][3]=glider[3][1]=glider[3][2]=glider[3][3]=1
    frames = game_of_life(glider, 4)
    print("\nGame of Life (glider):")
    for i, f in enumerate(frames):
        print(f"Step {i}:")
        for row in f: print("  " + "".join("█" if c else "·" for c in row))

if __name__ == "__main__": main()
