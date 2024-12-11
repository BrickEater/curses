import curses

# Take a 2d array as a grid where each object within the array represents
# the window id and create a window layout


def grid(win, arr, data):
    maxy, maxx = win.getmaxyx()
    grid_x = len(arr[0])
    grid_y = len(arr)
    grid_cell_size = (maxy // grid_y), (maxx // grid_x)
    value_coordinates = {}
    square_dimensions = {}
    windows = {}

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

    # Calculate the shift between the first and last point of each rectangle and
    # store these values and the length and width of each window
    for key, value in value_coordinates.items():
        square_dimensions[key] = [value[1][0] - value[0][0], value[1][1] - value[0][1]]

    # Calculate the length and width of each grid cells in terminal cells
    # Define each window by the length and with of grid cells
    # Find the starting point to draw the windows
    for key in value_coordinates:
        val_coor = value_coordinates[key]
        sq_dim = square_dimensions[key]

        window_starting_location = (
            grid_cell_size[0] * val_coor[0][0],
            grid_cell_size[1] * val_coor[0][1],
        )

        window_height = grid_cell_size[0] * sq_dim[0]
        window_width = grid_cell_size[1] * sq_dim[1]

        new_window = curses.newwin(
            window_height,
            window_width,
            window_starting_location[0],
            window_starting_location[1],
        )
        new_window.box()
        title = f" {data[key]} "
        new_window.addstr(0, 1, title)
        windows[data[key]] = new_window

    return windows


grid_layout = [
    [1, 2, 2],
    [1, 2, 2],
    [1, 2, 2],
    [3, 3, 3],
]
# grid_layout = [[1], [2], [3]]
# grid_layout = [
#     [1, 2],
# ]

window_names = {
    1: "main",
    2: "side",
    3: "footer",
}


screen = curses.initscr()

windows = grid(screen, grid_layout, window_names)

for win in windows.values():
    win.refresh()

windows["side"].addstr(1, 1, "testing")
windows["side"].refresh()

curses.napms(2000)
curses.endwin()
