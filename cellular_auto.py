#!/usr/bin/env python3
"""Cellular Automata - 1D and 2D (Game of Life) simulation."""
import sys, time

def rule_1d(rule_num, width=80, steps=40):
    rule = [(rule_num >> i) & 1 for i in range(8)]
    state = [0] * width; state[width // 2] = 1
    lines = []
    for _ in range(steps):
        lines.append("".join("█" if c else " " for c in state))
        new = [0] * width
        for i in range(width):
            l = state[(i-1) % width]; c = state[i]; r = state[(i+1) % width]
            new[i] = rule[(l << 2) | (c << 1) | r]
        state = new
    return lines

def game_of_life(grid, steps=10):
    rows, cols = len(grid), len(grid[0]); frames = []
    for _ in range(steps):
        frames.append(["".join("█" if c else "·" for c in row) for row in grid])
        new = [[0]*cols for _ in range(rows)]
        for r in range(rows):
            for c in range(cols):
                n = sum(grid[(r+dr)%rows][(c+dc)%cols] for dr in (-1,0,1) for dc in (-1,0,1) if (dr,dc) != (0,0))
                new[r][c] = 1 if (grid[r][c] and n in (2,3)) or (not grid[r][c] and n == 3) else 0
        grid = new
    return frames

def main():
    print("=== Cellular Automata ===\n")
    print("Rule 30 (1D):")
    for line in rule_1d(30, 60, 15): print(f"  {line}")
    print("\nGame of Life (glider):")
    grid = [[0]*20 for _ in range(15)]
    grid[1][2]=1; grid[2][3]=1; grid[3][1]=grid[3][2]=grid[3][3]=1
    frames = game_of_life(grid, 5)
    for i, frame in enumerate(frames):
        print(f"  Step {i}:")
        for row in frame: print(f"    {row}")

if __name__ == "__main__":
    rule = int(sys.argv[1]) if len(sys.argv) > 1 else None
    if rule is not None:
        for line in rule_1d(rule): print(line)
    else: main()
