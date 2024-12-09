import curses


def task_card(y, x):
    height = 30
    width = 70
    y_position = (y // 2) - (height // 2)
    x_position = (x // 2) - (width // 2)
    card = curses.newwin(height, width, y_position, x_position)
    card.box()
    card.refresh()
    card.getch()


def main():
    screen = curses.initscr()
    maxy, maxx = screen.getmaxyx()
    task_card(maxy, maxx)

    curses.endwin()


if __name__ == "__main__":
    main()
