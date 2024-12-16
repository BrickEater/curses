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
    # No duplicate names can be passed because the names are
    # parsed and used as keys in another dictionary. Duplicates will cause
    # an error since dictionaries require unique keys.
    names_list = list(window_names.values())
    if len(names_list) != len(set(names_list)):
        raise ValueError(
            f"Duplicate window names found in 'window_names': {window_names}"
        )


def error_check_for_equal_array_lengths(window_layout: List[List[int]]):
    """
    Validate that all lists are of equal length.

    Args:
        window_layout (List[List[int]]): A 2D array where each integer represents a window ID.

    Raises:
        ValueError: If any list is not of equal length to the other lists.
    """
    # Without this check, if a list is passed that is shorter or longer than
    # the others, the window rendering will be incorrect. Better to throw
    # an error with an explanation
    for rows in window_layout:
        if len(rows) != len(window_layout[0]):
            raise ValueError(
                f"Irregular list length found in 'window_layout': {window_layout}"
            )


def error_check_for_correct_window_formatting(window_layout: List[List[int]]):
    """
    Validate that all occurrences of each window ID in the 2D layout are adjacent.

    Args:
        window_layout (List[List[int]]): A 2D array where each integer represents a window ID.

    Raises:
        ValueError: If any window ID is repeated but not adjacent to other occurrences of the same ID.
    """
    # All window IDs need to be adjacent to eachother because of how the window
    # diameters are measured. The me define_window_length_and_width() functon
    # takes the top left and bottom right corners and measures the shift between
    # the two of them to assume a rectangle. If a window ID is misplaced, some IDs
    # may be outside of the rectangle area and the window will not render correctly.
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
                    raise ValueError(
                        f"Non-adjacent segments detected for window ID in 'window_layout': {window_layout}"
                    )

                coordinates[value].append((y, x))
            else:
                coordinates[value] = [(y, x)]


# Utility Functions-------------------------------------------------------------
def define_window_key_points(window_layout: List[List[int]]) -> Dict[int, Tuple]:
    """
    Find the top-left and bottom-right corners for each unique window ID in the layout.

    Args:
        window_layout (List[List[int]]): A 2D array where each integer represents a window ID.

    Returns:
        Dict[int, Tuple]: A dictionary where the keys are window IDs, and the values are tuples
                          containing the coordinates of the top-left and bottom-right corners of
                          the window's area.
    """
    # The top left and bottom right corners of the window layout is needed
    # to then calculate the dimentions with define_window_length_and_width()
    #
    # It should be noted that the +1s are needed because the top left corner
    # is what's used to refrense a terminal cell. Without these, the bottom
    # and right sides will not be drawn correctly.
    window_diagonal_corners = {}
    for y in range(len(window_layout)):
        for x in range(len(window_layout[y])):
            value = window_layout[y][x]
            if value not in window_diagonal_corners:
                window_diagonal_corners[value] = [(y, x), (y + 1, x + 1)]
            else:
                window_diagonal_corners[value][1] = (y + 1, x + 1)
    return window_diagonal_corners


def define_window_length_and_width(
    window_diagonal_corners: Dict[int, Tuple],
) -> Dict[int, Tuple]:
    """
    Find the window length and width by using the shift between the top left and bottom right window corners.

    Args:
        window_diagonal_corners (Dict[int, Tuple]): The top left and bottom right corners of a window's grid layout.

    Returns:
        Dict[int, Tuple]: A dictionary where the keys are window IDs, and the values are tuples
                          of the length and width of each window, measured with the layout grid
                          cell as the unit of measurment.
    """
    # You take the dimensions of the windows as a ratio relative to the
    # terminal length and width from getmaxyx(). You can then calculate
    # the exact termainl cells where to start and how long and wide the
    # curses window needs to be.
    window_dimensions = {}
    for key, value in window_diagonal_corners.items():
        window_dimensions[key] = [value[1][0] - value[0][0], value[1][1] - value[0][1]]
    return window_dimensions


# Main function-----------------------------------------------------------------
def grid(
    win: curses.window,
    window_layout: List[List[int]],
    window_names: Optional[Dict[int, str]] = None,
) -> Dict[str, curses.window]:
    """
    Take a 2D array and create a window layout

    Args:
        win (curses.window): A curses window
        window_layout (List[List[int]]): A 2D array where each integer represents a window ID.
        window_names (Dict[int, str]): A dictionary mapping window IDs (keys) to their corresponding names (values).

    Returns:
        Dict[str, curses.window]: A dictionary where the keys are the window names and the values
                                  are the curses windows.
    """
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
    window_diagonal_corners = {}
    window_dimensions = {}
    windows = {}

    window_diagonal_corners = define_window_key_points(window_layout)

    window_dimensions = define_window_length_and_width(window_diagonal_corners)

    # The grid_cell_size variable is used as a unit of measurement to make
    # creating the windows simple and ensure consistancy across all windows.
    for key in window_diagonal_corners:
        corner_coordinates = window_diagonal_corners[key]
        win_dimensions = window_dimensions[key]

        window_starting_location = (
            grid_cell_size[0] * corner_coordinates[0][0],
            grid_cell_size[1] * corner_coordinates[0][1],
        )
        print(corner_coordinates[0][1])

        window_height = grid_cell_size[0] * win_dimensions[0]
        window_width = grid_cell_size[1] * win_dimensions[1]

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
    1: "main",
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

    windows["main"].getch()


wrapper(main)
