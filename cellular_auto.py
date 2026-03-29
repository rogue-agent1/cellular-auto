#!/usr/bin/env python3
"""Cellular automaton: 1D elementary and 2D Game of Life."""

def elementary_1d(rule, width=80, steps=40, init=None):
    if init is None:
        state = [0] * width
        state[width // 2] = 1
    else:
        state = list(init)
    history = [state[:]]
    for _ in range(steps):
        new = [0] * width
        for i in range(width):
            left = state[(i-1) % width]
            center = state[i]
            right = state[(i+1) % width]
            idx = (left << 2) | (center << 1) | right
            new[i] = (rule >> idx) & 1
        state = new
        history.append(state[:])
    return history

class GameOfLife:
    def __init__(self, width, height):
        self.w, self.h = width, height
        self.grid = [[0]*width for _ in range(height)]

    def set(self, x, y, val=1):
        self.grid[y % self.h][x % self.w] = val

    def get(self, x, y):
        return self.grid[y % self.h][x % self.w]

    def neighbors(self, x, y):
        count = 0
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx == 0 and dy == 0: continue
                count += self.get(x+dx, y+dy)
        return count

    def step(self):
        new = [[0]*self.w for _ in range(self.h)]
        for y in range(self.h):
            for x in range(self.w):
                n = self.neighbors(x, y)
                if self.grid[y][x]:
                    new[y][x] = 1 if n in (2, 3) else 0
                else:
                    new[y][x] = 1 if n == 3 else 0
        self.grid = new

    def population(self):
        return sum(sum(row) for row in self.grid)

    def add_pattern(self, x, y, pattern):
        for dy, row in enumerate(pattern):
            for dx, cell in enumerate(row):
                if cell: self.set(x+dx, y+dy)

if __name__ == "__main__":
    history = elementary_1d(110, width=40, steps=20)
    for row in history:
        print("".join("█" if c else " " for c in row))

def test():
    # Rule 110
    h = elementary_1d(110, width=20, steps=10)
    assert len(h) == 11
    assert h[0][10] == 1  # center cell
    # Rule 30
    h2 = elementary_1d(30, width=20, steps=5)
    assert len(h2) == 6
    # Game of Life - blinker
    g = GameOfLife(10, 10)
    g.set(4, 5); g.set(5, 5); g.set(6, 5)
    assert g.population() == 3
    g.step()
    # Blinker should rotate
    assert g.get(5, 4) == 1
    assert g.get(5, 5) == 1
    assert g.get(5, 6) == 1
    assert g.population() == 3
    # Block (still life)
    g2 = GameOfLife(10, 10)
    g2.set(4, 4); g2.set(5, 4); g2.set(4, 5); g2.set(5, 5)
    pop = g2.population()
    g2.step()
    assert g2.population() == pop
    print("  cellular_auto: ALL TESTS PASSED")
