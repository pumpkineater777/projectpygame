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


def do_path(coords):
    n = len(coords)
    x = []
    for elem in coords:
        x.append(elem)
    coords = []
    for i in range(0, n, 2):
        coords.append([x[i], x[i + 1]])
    post_x, post_y = coords[0]
    A = []
    n = len(coords)
    for i in range(1, n):
        r = ((coords[i][0] - post_x) ** 2 + (coords[i][1] - post_y) ** 2) ** 0.5
        if coords[i][0] - post_x == 0:
            if coords[i][1] - post_y > 0:
                sin = 1
                cos = 0
            else:
                sin = -1
                cos = 0
        elif coords[i][1] - post_y == 0:
            if coords[i][1] - post_y > 0:
                cos = 1
                sin = 0
            else:
                cos = -1
                sin = 0
        else:
            cos = (coords[i][0] - post_x) / r
            sin = (coords[i][1] - post_y) / r
        post_x, post_y = coords[i][0], coords[i][1]
        A.append([post_x, post_y, cos, sin, r])
    step = 5
    B = []
    print(A)
    for elem in A:
        x, y, cos, sin, r = elem
        j = 0
        while j <= r / step:
            x0 = x
            y0 = y
            x += cos * step
            y += sin * step
            j += 1
            B.append([x - x0, y - y0])
    return B

