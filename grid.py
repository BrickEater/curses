import curses


def grid(win, arr):
    maxy, maxx = win.getmaxyx()
    grid_width = len(arr[0])
    grid_length = len(arr)
    value_coordinates = {}
    square_dimensions = {}
    windows = []

    for y in range(len(arr)):
        for x in range(len(arr[y])):
            value = arr[y][x]
            if value not in value_coordinates:
                value_coordinates[value] = [(y, x), (y + 1, x + 1)]
            else:
                value_coordinates[value][1] = (y + 1, x + 1)

    for key, value in value_coordinates.items():
        square_dimensions[key] = [value[1][0] - value[0][0], value[1][1] - value[0][1]]

    for (key1, value1), (key2, value2) in zip(
        value_coordinates.items(), square_dimensions.items()
    ):
        window_starting_location = (
            maxy * (value1[0][0] * 100 // grid_length + 1) // 100,
            maxx * (value1[0][1] * 100 // grid_length) // 100,
        )
        window_height = (maxy // grid_length) * value2[0]
        window_width = (maxx // grid_width) * value2[1]
        window = curses.newwin(
            window_height,
            window_width,
            window_starting_location[0],
            window_starting_location[1],
        )
        window.box()
        windows.append(window)

    return windows


array = [
    [1, 2, 2],
    [1, 2, 2],
    [3, 3, 3],
]
# array = [[1], [2], [3]]
# array = [[1, 2, 3], [1, 2, 3]]


screen = curses.initscr()

windows = grid(screen, array)
for i, win in enumerate(windows):
    h, w = win.getmaxyx()  # Get height and width
    y, x = win.getbegyx()  # Get starting position (y, x)
    print(f"Window {i+1}: Height={h}, Width={w}, Position=({y}, {x})")

for win in windows:
    win.refresh()

windows[0].getch()

curses.endwin()
