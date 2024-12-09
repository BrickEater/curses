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

    """
    for something in something:
        window_id = It would be easier to grab this at the beginning of the loop
        start_location = I need this so I know where to put the window
        window_height = I need to calculate this with a ratio of the grid length and the window length
        window_width = Same thing with the width
    """

    window1_starting_location = (
        maxy * value_coordinates[1][0][0],
        maxx * value_coordinates[1][0][1],
    )
    window1_height = (maxy // grid_length) * square_dimensions[1][0]
    window1_width = (maxx // grid_width) * square_dimensions[1][1]
    win1 = curses.newwin(
        window1_height,
        window1_width,
        window1_starting_location[0],
        window1_starting_location[1],
    )
    win1.box()
    windows.append(win1)

    window2_starting_location = (
        maxy * (value_coordinates[2][0][0] * 100 // grid_length) // 100,
        maxx * (value_coordinates[2][0][1] * 100 // grid_width) // 100,
    )
    window2_height = (maxy // grid_length) * square_dimensions[2][0]
    window2_width = (maxx // grid_width) * square_dimensions[2][1]
    win2 = curses.newwin(
        window2_height,
        window2_width,
        window2_starting_location[0],
        window2_starting_location[1],
    )
    win2.box()
    windows.append(win2)

    window3_starting_location = (
        maxy * (value_coordinates[3][0][0] * 100 // grid_length) // 100,
        maxx * (value_coordinates[3][0][1] * 100 // grid_width) // 100,
    )
    window3_height = (maxy // grid_length) * square_dimensions[3][0]
    window3_width = (maxx // grid_width) * square_dimensions[3][1]
    win3 = curses.newwin(
        window3_height,
        window3_width,
        window3_starting_location[0],
        window3_starting_location[1],
    )
    win3.box()
    windows.append(win3)

    # for i in range(len(square_dimensions)):
    #     win1 = win.subwin(5, 5, i * 6, 5)  # Example positioning of windows
    #     win1.border()
    #     windows.append(win1)  # Append each window to the list

    return windows  # Return the list of windows


array = [
    [1, 1, 2],
    [1, 1, 2],
    [3, 3, 3],
]


screen = curses.initscr()

windows = grid(screen, array)

for win in windows:
    win.refresh()

windows[0].getch()

curses.endwin()
