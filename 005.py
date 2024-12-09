import curses

screen = curses.initscr()
num_rows, num_cols = screen.getmaxyx()


def print_center(message):
    middle_row = int(num_rows / 2)

    half_length_of_message = int(len(message) / 2)
    middle_column = int(num_cols / 2)
    x_position = middle_column - half_length_of_message

    screen.addstr(middle_row, x_position, message)
    screen.refresh()


print_center("Hello, from the center!")

curses.napms(3000)
curses.endwin()
