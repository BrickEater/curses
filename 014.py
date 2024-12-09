# form.py
import curses


def main(stdscr):
    # Disable cursor and enable keypad input
    curses.curs_set(1)
    stdscr.keypad(True)

    # Field coordinates and content
    fields = [("Name", 1, 2), ("Age", 3, 2), ("Email", 5, 2)]
    data = [""] * len(fields)
    current_field = 0

    def draw_form():
        stdscr.clear()
        for i, (label, y, x) in enumerate(fields):
            stdscr.addstr(y, x, f"{label}: ")
            stdscr.addstr(y, x + len(label) + 2, data[i])
            if i == current_field:
                stdscr.addstr(y, x + len(label) + 2 + len(data[i]), "_")
        stdscr.refresh()

    while True:
        draw_form()
        key = stdscr.getch()

        if key == curses.KEY_UP:
            current_field = (current_field - 1) % len(fields)
        elif key == curses.KEY_DOWN:
            current_field = (current_field + 1) % len(fields)
        elif key in (curses.KEY_ENTER, 10, 13):  # Enter key
            break
        elif key in (curses.KEY_BACKSPACE, 127):
            if data[current_field]:
                data[current_field] = data[current_field][:-1]
        elif 32 <= key <= 126:  # Printable ASCII characters
            data[current_field] += chr(key)

    stdscr.clear()
    stdscr.addstr(1, 2, "Form Submitted:")
    for i, value in enumerate(data):
        stdscr.addstr(3 + i, 4, f"{fields[i][0]}: {value}")
    stdscr.refresh()
    stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(main)
