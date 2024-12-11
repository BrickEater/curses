# TODO:
# This is broken
# I think it's because of how I'm calculating the screen dimensions
# I can see that when I print the parameters of the windows created, the width
# compared to where they start are not correct

# NOTE:
# I've realized I should measure how many terminal cells fit into each
# grid cell so that I can define the length and with of each window
# with grid cells. This way I don't need to do dumb math and can just say
# width: 3 cells, hight: 2 cells
# Also, I can take the difference the maximum grid cells within the screen
# and, if the difference is an even number, I can make it a magin value so
# the windows are centered on the screen. This can avoid having a large gap
# on the right and bottom sides of the screen

# NOTE:
# I should also change the function to take a list/dictionary/array, whatever, with
#  key value pairs of the window id and window name so the windows are created with
# a name and are easier to refrense once created


import curses

# Take a 2d array as a grid where each object within the array represents
# the window id and create a window layout


def grid(win, arr):
    maxy, maxx = win.getmaxyx()
    grid_width = len(arr[0])
    grid_length = len(arr)
    value_coordinates = {}
    square_dimensions = {}
    windows = []

    # Find the top left and bottom right points of each window on the grid
    # Itterates through the grid and stores the first point of a window
    # store the last point of the window
    # this is to calculate the shift between the points and structure a rectangle
    for y in range(len(arr)):
        for x in range(len(arr[y])):
            value = arr[y][x]
            if value not in value_coordinates:
                value_coordinates[value] = [(y, x), (y + 1, x + 1)]
            else:
                value_coordinates[value][1] = (y + 1, x + 1)

    print(value_coordinates)
    # Calculate the shift between the first and last point of each rectangle and
    # store these values and the length and width of each window
    for key, value in value_coordinates.items():
        square_dimensions[key] = [value[1][0] - value[0][0], value[1][1] - value[0][1]]

    # Calculate the length and width of each grid cells in terminal cells
    # Define each window by the length and with of grid cells
    # Find the starting point to draw the windows
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
    [1, 2, 2],
    [3, 3, 3],
]
# array = [[1], [2], [3]]
# array = [
#     [1, 1, 2],
#     [1, 1, 2],
#     [1, 1, 2],
#     [3, 3, 3],
# ]


screen = curses.initscr()

windows = grid(screen, array)

for win in windows:
    win.refresh()

curses.napms(2000)
curses.endwin()

print(screen.getmaxyx())
for i, win in enumerate(windows):
    h, w = win.getmaxyx()  # Get height and width
    y, x = win.getbegyx()  # Get starting position (y, x)
    print(f"Window {i+1}: Height={h}, Width={w}, Position=({y}, {x})")
