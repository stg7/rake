#!/usr/bin/env python3
"""
    rake = rescue snake

    author: Steve Göring
    contact: stg7@gmx.de
    2014
"""
"""
    This file is part of rake.

    rake is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    rake is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with rake.  If not, see <http://www.gnu.org/licenses/>.
"""

import argparse
import pygame
import math
import random
import sys
import time

from log import *

size_x = 1024
size_y = 512
tile_size = 8
k = 512

"""
diamond square algo, see http://en.wikipedia.org/wiki/Diamond-square_algorithm
"""


def init_map(k):
    gmap = [
        [0 for i in range(0, size_y // tile_size)] for j in range(0, size_x // tile_size)
    ]
    gmap[0][0] = random.randint(0, 256)
    gmap[-1][0] = random.randint(0, 256)
    gmap[0][-1] = random.randint(0, 256)
    gmap[-1][-1] = random.randint(0, 256)
    return gmap


def diamond_square_it(gmap, x1, y1, x2, y2, range_v, level):

    while level >= 1:
        # diamands
        for i in range(x1 + level, x2, level):
            for j in range(y1 + level, y2, level):
                a = gmap[i - level][j - level]
                b = gmap[i][j - level]
                c = gmap[i - level][j]
                d = gmap[i][j]
                gmap[i - level // 2][j - level // 2] = (a + b + c + d) / 4 + (2 * random.random() - 1) * range_v

        # squares
        for i in range(x1 + 2 * level, x2, level):
            for j in range(y1 + 2 * level, y2, level):
                a = gmap[i - level][j - level]
                b = gmap[i][j - level]
                c = gmap[i - level][j]
                d = gmap[i][j]
                e = gmap[i - level // 2][j - level // 2]

                gmap[i - level][j - level // 2] = (a + c + e + gmap[i - 3 * level // 2][j - level // 2]) / 4 + (2 * random.random() - 1) * range_v
                gmap[i - level // 2][j - level] = (a + b + e + gmap[i - level // 2][j - 3 * level // 2]) / 4 + (2 * random.random() - 1) * range_v
        level //= 2
        range_v //= 2

    return gmap


def update_map(gmap, k):
    # return diamond_square(gmap, 0, 0, len(gmap) - 1, len(gmap[0]) -1, k)
    return diamond_square_it(gmap, 0, 0, len(gmap) - 1, len(gmap[0]) - 1, k, len(gmap))


def normalize_map(gmap, scale_min=0.001, scale_max=0.001):
    lis = []
    for i in gmap:
        lis += i
    lis.sort()

    # normalize gamemap
    min_v = lis[int(scale_min * (len(lis) - 1))]
    max_v = lis[-int(scale_max * (len(lis) - 1))]

    gmap = [[max(min_v, y) for y in x] for x in gmap]

    gmap = [[min(max_v, y) for y in x] for x in gmap]

    gmap = [[255 * (y - min_v) / (max_v - min_v) for y in x] for x in gmap]

    return gmap


def handle_key(direction):
    if pygame.key.get_pressed()[pygame.K_UP] != 0 and direction[0] != 1:
        return (-1, 0)

    if pygame.key.get_pressed()[pygame.K_LEFT] != 0 and direction[1] != 1:
        return (0, -1)

    if pygame.key.get_pressed()[pygame.K_RIGHT] != 0 and direction[1] != -1:
        return (0, 1)

    if pygame.key.get_pressed()[pygame.K_DOWN] != 0 and direction[0] != -1:
        return (1, 0)

    return direction


def handle_event():
    event = pygame.event.poll()
    if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE] != 0:
        return True
    if event.type == pygame.MOUSEMOTION:
        pass
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        lDbg("You pressed the left mouse button at (%d, %d)" % event.pos)
    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
        lDbg("You released the left mouse button at (%d, %d)" % event.pos)
    return False


def draw_map(screen, gmap, lower_limit, upper_limit):
    for i in range(1, len(gmap) - 1):
        for j in range(1, len(gmap[i]) - 1):
            x = tile_size * i
            y = tile_size * j
            c = int(gmap[i][j])
            color = (c, c, 0)
            if c < lower_limit:
                color = (c, c, 255 - c)
            if c > upper_limit:
                color = (c, c, c)

            pygame.draw.rect(screen, color, (x, y, tile_size, tile_size), 0)


def intro(screen, upper_limit=200):
    myfont = pygame.font.SysFont("monospace", 40)
    clock = pygame.time.Clock()
    for i in range(10, 200, 10):
        gamemap = normalize_map(update_map(init_map(k), k))
        draw_map(screen, gamemap, i, upper_limit)
        label = myfont.render("rake - rescue snake..", 1, (255, 0, 0))
        screen.blit(label, (100, 100))
        pygame.display.flip()
        msElapsed = clock.tick(30)


def outtro(screen, round_nr, end, upper_limit=200):
    myfont = pygame.font.SysFont("monospace", 40)
    label = myfont.render("you " + end + " in round.." + str(round_nr), 1, (255, 0, 0))

    clock = pygame.time.Clock()
    run = 0
    while not handle_event():
        if pygame.key.get_pressed()[pygame.K_y] != 0:
            return True

        if pygame.key.get_pressed()[pygame.K_n] != 0:
            return False

        gamemap = normalize_map(update_map(init_map(k), k))
        draw_map(screen, gamemap, 20, upper_limit)

        if run > 200:
            label = myfont.render("play again (y) or quit (n)", 1, (255, 0, 0))

        screen.blit(label, (100, 100))
        pygame.display.flip()
        msElapsed = clock.tick(30)
        run += 10

    return False


def play(screen, lower_limit=10, upper_limit=200):
    clock = pygame.time.Clock()
    myfont = pygame.font.SysFont("monospace", 40)
    for round_nr in range(1, 100):
        gamemap = normalize_map(update_map(init_map(k), k))
        pos_x = random.randint(1, len(gamemap) - 1)
        pos_y = random.randint(1, len(gamemap[0]) - 1)
        direction = (0, 0)
        run = 0
        waypoints = [(pos_x, pos_y)]
        end = "start"
        while end not in ["loose", "win"]:

            if handle_event() is True:
                end = "exit"
                break

            direction = handle_key(direction)

            if direction != (0, 0):
                pos_x = pos_x + direction[1]
                pos_y = pos_y + direction[0]
                end = "exit"
                if pos_x not in range(1, len(gamemap) - 1) or pos_y not in range(1, len(gamemap[0]) - 1):
                    end = "loose"
                if gamemap[pos_x][pos_y] > upper_limit:
                    end = "win"
                if gamemap[pos_x][pos_y] < lower_limit:
                    end = "loose"
                if (pos_x, pos_y) in waypoints:
                    end = "loose"

                waypoints.append((pos_x, pos_y))

            screen.fill((0, 0, 0))

            draw_map(screen, gamemap, lower_limit, upper_limit)

            for (w_x, w_y) in waypoints:
                pygame.draw.rect(screen, (255, 0, 0), (w_x * tile_size, w_y * tile_size, tile_size, tile_size), 0)

            if end == "start":
                # render text
                label = myfont.render("prepare for round.." + str(round_nr), 1, (255, 0, 0))
                screen.blit(label, (100, 100))

            pygame.display.flip()
            msElapsed = clock.tick(30)

            if direction != (0, 0):
                if run % 20 == 0:
                    lower_limit += 10
                run += 1
        if end in ["loose", "exit"]:
            return (round_nr, end)
        lower_limit = 10


def main():
    # argument parsing
    parser = argparse.ArgumentParser(description='rake = rescue snake', epilog="stg7 2014")
    parser.add_argument('-s', dest='seed', type=int, default=-1, help='random seed')

    argsdict = vars(parser.parse_args())

    if argsdict["seed"] != -1:
        random.seed(argsdict["seed"])

    lInfo("start game")

    pygame.init()
    screen = pygame.display.set_mode((size_x, size_y))
    pygame.display.set_caption("rake = rescue snake -- stg7 2014")

    intro(screen)

    again = True
    while again is True:
        (round_nr, end) = play(screen)
        again = outtro(screen, round_nr, end)

    lInfo("game done.")


if __name__ == "__main__":
    main()
