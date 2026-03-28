#!/usr/bin/env python3
"""cellular_auto - 1D cellular automata (Wolfram rules)."""
import sys

def step(cells, rule):
    n=len(cells); new=[0]*n
    for i in range(n):
        l=cells[(i-1)%n]; c=cells[i]; r=cells[(i+1)%n]
        idx=l*4+c*2+r
        new[i]=(rule>>idx)&1
    return new

def run(rule=30, width=80, steps=40, init=None):
    cells=[0]*width
    if init: 
        for i in init: cells[i%width]=1
    else: cells[width//2]=1
    print(f"Rule {rule}:")
    for _ in range(steps):
        print(''.join('█' if c else ' ' for c in cells))
        cells=step(cells, rule)

def main():
    args=sys.argv[1:]
    rule=int(args[0]) if args and args[0].isdigit() else 30
    width=int(args[args.index('-w')+1]) if '-w' in args else 80
    steps=int(args[args.index('-s')+1]) if '-s' in args else 40
    if '-h' in args and not args[0].isdigit():
        print("Usage: cellular_auto.py [RULE] [-w WIDTH] [-s STEPS]"); return
    run(rule, width, steps)

if __name__=='__main__': main()
