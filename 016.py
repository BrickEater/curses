import curses
from collections import Counter


def make_grid(win, arr):
    maxy, maxx = win.getmaxyx()
    flatten = [item for sublist in arr for item in sublist]
    counter = Counter(flatten)
    unique_tuples = [(value, count) for value, count in counter.items()]

    for i in range(len(arr)):
        for j in range(len(arr[i])):
            win.addstr(str(arr[i][j]))
        win.addstr("\n")

    win.addstr(str(unique_tuples))


an_array = [[1, 1, 2], [1, 1, 2], [3, 3, 3]]


screen = curses.initscr()
make_grid(screen, an_array)
screen.getch()
curses.endwin()
