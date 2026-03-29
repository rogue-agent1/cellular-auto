#!/usr/bin/env python3
"""cellular_auto: 1D/2D cellular automata (Wolfram rules + Game of Life)."""
import sys

def wolfram_rule(rule_num, width=31, steps=15, init=None):
    if init is None:
        state = [0] * width
        state[width // 2] = 1
    else:
        state = list(init)
    history = [state[:]]
    for _ in range(steps):
        new = [0] * width
        for i in range(width):
            l = state[(i-1) % width]
            c = state[i]
            r = state[(i+1) % width]
            idx = (l << 2) | (c << 1) | r
            new[i] = (rule_num >> idx) & 1
        state = new
        history.append(state[:])
    return history

def game_of_life(grid, steps=1):
    rows, cols = len(grid), len(grid[0])
    for _ in range(steps):
        new = [[0]*cols for _ in range(rows)]
        for r in range(rows):
            for c in range(cols):
                neighbors = sum(
                    grid[(r+dr)%rows][(c+dc)%cols]
                    for dr in (-1,0,1) for dc in (-1,0,1)
                    if (dr, dc) != (0, 0)
                )
                if grid[r][c] == 1:
                    new[r][c] = 1 if neighbors in (2, 3) else 0
                else:
                    new[r][c] = 1 if neighbors == 3 else 0
        grid = new
    return grid

def render(state):
    return "".join("#" if c else "." for c in state)

def test():
    # Rule 30
    h = wolfram_rule(30, width=11, steps=5)
    assert len(h) == 6
    assert h[0][5] == 1  # Center cell
    assert sum(h[1]) > 1  # Spreads
    # Rule 110 (Turing complete)
    h2 = wolfram_rule(110, width=11, steps=3)
    assert len(h2) == 4
    # Game of Life: blinker
    grid = [
        [0,0,0,0,0],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [0,0,0,0,0],
    ]
    g1 = game_of_life(grid, 1)
    assert g1[2][1] == 1 and g1[2][2] == 1 and g1[2][3] == 1
    assert g1[1][2] == 0  # Horizontal now
    # Period 2
    g2 = game_of_life(grid, 2)
    assert g2 == grid
    # Block (still life)
    block = [
        [0,0,0,0],
        [0,1,1,0],
        [0,1,1,0],
        [0,0,0,0],
    ]
    assert game_of_life(block, 1) == block
    print("All tests passed!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test": test()
    else: print("Usage: cellular_auto.py test")
