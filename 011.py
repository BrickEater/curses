import curses


class Card:
    def __init__(self):
        self.fields = {"Name": "", "Age": "", "Role": ""}


def draw_card(win, card, current_field):
    h, w = win.getmaxyx()
    win.clear()
    win.box()

    y_offset = 2
    for i, (field, value) in enumerate(card.fields.items()):
        highlight = curses.A_REVERSE if i == current_field else curses.A_NORMAL
        win.addstr(y_offset, 2, f"{field}: {value}", highlight)
        y_offset += 2

    win.addstr(h - 2, 2, "Press TAB to navigate, ENTER to submit")
    win.refresh()


def handle_input(win, field_name):
    curses.echo()
    win.addstr(1, 1, f"Enter {field_name}: ")
    win.refresh()
    input_str = win.getstr().decode("utf-8")
    curses.noecho()
    return input_str


def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    card = Card()
    current_field = 0
    fields = list(card.fields.keys())

    while True:
        draw_card(stdscr, card, current_field)

        key = stdscr.getch()
        if key == 9:
            current_field = (current_field + 1) % len(fields)
        elif key == curses.KEY_ENTER or key in [10, 13]:
            input_win = curses.newwin(3, 40, 10, 10)
            input_win.box()
            input_win.refresh()
            card.fields[fields[current_field]] = handle_input(
                input_win, fields[current_field]
            )
            del input_win
        elif key == 27:  # ESC key to exit
            break


if __name__ == "__main__":
    curses.wrapper(main)
