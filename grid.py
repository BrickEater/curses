# TODO:
# Write docstrings for each functino
# Write comments explaining the why of each function
# Add one more error handling function checking if the name dictinoary
# is longer than the window layout dictionary.
# That, or write some better code to not have to worry about that


import curses
from curses import wrapper
from typing import Optional, Dict, List, Tuple


# Error Handling----------------------------------------------------------------
def error_check_for_name_duplication(window_names: Dict[int, str]):
    """
    Validate that all window names are unique.

    Args:
        window_names (Dict[int, str]): A dictionary mapping window IDs (keys)
        to their corresponding names (values).

    Raises:
        ValueError: If any names are duplicated in the dictionary.
    """
    names_list = list(window_names.values())
    if len(names_list) != len(set(names_list)):
        raise ValueError(
            f"Duplicate window names found in 'window_names': {window_names}"
        )


def error_check_for_equal_array_lengths(window_layout: List[List[int]]):
    """
    Validate that all lists are of equal length.

    Args:
        window_layout (List[List[int]]): A list of lists, often referred to as a 2D array.

    Raises:
        ValueError: If any list is not of equal length to the other lists.
    """
    for rows in window_layout:
        if len(rows) != len(window_layout[0]):
            raise ValueError(
                f"Irregular list length found in 'window_layout': {window_layout}"
            )


def error_check_for_correct_window_formatting(window_layout: List[List[int]]):
    coordinates = {}
    for y, row in enumerate(window_layout):
        for x, value in enumerate(row):
            if value in coordinates:
                adjacent_found = False
                for prev_y, prev_x in coordinates[value]:
                    if (abs(prev_y - y) == 1 and prev_x == x) or (
                        abs(prev_x - x) == 1 and prev_y == y
                    ):
                        adjacent_found = True
                        break

                if not adjacent_found:
                    raise ValueError("Window IDs need to be adjacent to each other")

                coordinates[value].append((y, x))
            else:
                coordinates[value] = [(y, x)]


# Utility Functions-------------------------------------------------------------
def define_window_key_points(window_layout: List[List[int]]) -> Dict[int, Tuple]:
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
    value_coordinates: Dict[int, Tuple],
) -> Dict[int, Tuple]:
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

    value_coordinates = define_window_key_points(window_layout)

    square_dimensions = define_window_length_and_width(value_coordinates)

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


# Example Values----------------------------------------------------------------
grid_layout = [
    [1, 2, 2],
    [1, 2, 2],
    [1, 2, 2],
    [3, 3, 3],
]
# grid_layout = [[1]]
# grid_layout = [
#     [1, 2, 2],
# ]
# grid_layout = [
#     [1, 2, 2],
#     [3, 4, 4],
# ]
# grid_layout = [
#     [1, 2, 3],
#     [4, 5, 6],
#     [7, 8, 9],
# ]

window_names = {
    1: "1",
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6",
    7: "7",
    8: "8",
    9: "9",
}


# Main init---------------------------------------------------------------------
def main(screen):
    screen = curses.initscr()
    screen.clear()

    windows = grid(screen, grid_layout, window_names)

    for win in windows.values():
        win.refresh()

    windows["1"].getch()


wrapper(main)
