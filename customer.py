'''import pygame as pg

class Customer(pg.sprite):
    def __init__(self, x, y):
9
50.83 6.81 67.62 36.77
63.5 39.97 84.92 43.56
58.5 80.91 101.31 45.89
38.63 123.69 130.03 32.65
18.75 146.56 149.42 25.55
5.53 160.81 110.56 34.18
2.5 191.97 92.86 60.07
3.53 250.84 73.30 41.76
15.72 290.59 36.38 23.6
'''
import math

n = int(input())
A = []
summ = 0
for i in range(n):
    x, y, deg, r = [float(elem) for elem in input().split()]
    summ += r
    A.append([x, y, deg, r])
step = 3
print('[')
for elem in A:
    x, y, deg, r = elem
    j = 0
    while j * step < r:
        x0 = x
        y0 = y
        x += math.cos(math.radians(deg)) * step
        y += math.sin(math.radians(deg)) * step
        j += 1
        print(f"({x - x0}, {y - y0}), ", end='')
print(']')
