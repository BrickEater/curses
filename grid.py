# TODO:
# I'm too tired to finish this
# I need to fix the few errors but then this is mostly done

# Take a 2d array as a grid where each object within the array represents
# the window id and create a window layout

import curses
from curses import wrapper
from typing import Optional, Dict, List, Tuple


# Error Handling----------------------------------------------------------------
def error_check_for_name_duplication(window_names: Dict[int, str]):
    names_list = list(window_names.values())
    if len(names_list) != len(set(names_list)):
        raise ValueError("Window names cannot be duplicated")


def error_check_for_equal_array_lengths(window_layout: List[List[int]]):
    for rows in window_layout:
        if len(rows) != len(window_layout[0]):
            raise ValueError("All list lengths must be equal")


def error_check_for_correct_window_formatting(window_layout: List[List[int]]):
    coordinates = {}
    for y, row in enumerate(window_layout):
        for x, value in enumerate(row):
            # If the value exists in coordinates
            if value in coordinates:
                # Check adjacency of the current coordinate to any previous ones
                adjacent_found = False
                for prev_y, prev_x in coordinates[value]:
                    # Check if the current coordinate is adjacent to any previous ones
                    if (abs(prev_y - y) == 1 and prev_x == x) or (
                        abs(prev_x - x) == 1 and prev_y == y
                    ):
                        adjacent_found = True
                        break

                # If no adjacent coordinates found, raise an error
                if not adjacent_found:
                    raise ValueError("Window IDs need to be adjacent to each other")

                # Append the current coordinate to the list
                coordinates[value].append((y, x))
            else:
                # If it's the first occurrence, initialize with the current coordinate
                coordinates[value] = [(y, x)]


# Utility Functions-------------------------------------------------------------
def define_window_key_points(window_layout: List[List[int]]) -> Dict[int, int]:
    value_coordinates = {}
    for y in range(len(window_layout)):
        for x in range(len(window_layout[y])):
            value = window_layout[y][x]
            if value not in value_coordinates:
                value_coordinates[value] = [(y, x), (y + 1, x + 1)]
            else:
                value_coordinates[value][1] = (y + 1, x + 1)
    return value_coordinates


def define_window_length_and_width(
    value_coordinates: Dict[int, Tuple[int, int]],
) -> Dict[int, int]:
    square_dimensions = {}
    for key, value in value_coordinates.items():
        square_dimensions[key] = [value[1][0] - value[0][0], value[1][1] - value[0][1]]
    return square_dimensions


# Main function-----------------------------------------------------------------
def grid(
    win: curses.window,
    window_layout: List[List[int]],
    window_names: Optional[Dict[int, str]] = None,
) -> Dict[str, curses.window]:
    if window_names:
        error_check_for_name_duplication(window_names)
    elif window_names is None:
        window_names = {}

    error_check_for_equal_array_lengths(window_layout)
    error_check_for_correct_window_formatting(window_layout)

    maxy, maxx = win.getmaxyx()
    grid_x = len(window_layout[0])
    grid_y = len(window_layout)
    grid_cell_size = (maxy // grid_y), (maxx // grid_x)
    value_coordinates = {}
    square_dimensions = {}
    windows = {}

    # Find the top left and bottom right points of each window on the grid
    # Itterates through the grid and stores the first point of a window
    # store the last point of the window
    # this is to calculate the shift between the points and structure a rectangle
    value_coordinates = define_window_key_points(window_layout)

    # Calculate the shift between the first and last point of each rectangle and
    # store these values and the length and width of each window
    square_dimensions = define_window_length_and_width(value_coordinates)

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
        title = f" {window_names[key]} "
        new_window.addstr(0, 1, title)
        windows[window_names[key]] = new_window

    return windows


# Configuration-----------------------------------------------------------------
grid_layout = [
    [1, 2, 2],
    [1, 2, 2],
    [1, 2, 2],
    [3, 3, 3],
]

window_names = {
    1: "main",
    2: "side",
    3: "footer",
    4: "something",
}


# Main init---------------------------------------------------------------------
def main(screen):
    screen = curses.initscr()
    screen.clear()

    windows = grid(screen, grid_layout, window_names)

    for win in windows.values():
        win.refresh()

    # windows["side"].addstr(1, 1, "testing")
    # windows["side"].refresh()

    windows["main"].getch()
    # curses.endwin()


wrapper(main)
