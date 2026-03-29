import argparse

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
    p = argparse.ArgumentParser(description="1D cellular automaton")
    p.add_argument("-r", "--rule", type=int, default=30)
    p.add_argument("-w", "--width", type=int, default=79)
    p.add_argument("-g", "--generations", type=int, default=40)
    p.add_argument("--alive", default="█")
    p.add_argument("--dead", default=" ")
    args = p.parse_args()
    cells = [0] * args.width
    cells[args.width // 2] = 1
    for _ in range(args.generations):
        print("".join(args.alive if c else args.dead for c in cells))
        cells = step(cells, args.rule)

if __name__ == "__main__":
    main()
