import curses


def make_window():
    window = curses.newwin(10, 10)
    window.box()


screen = curses.initscr()

# make_window()
window = curses.newwin(10, 10)
window.box()
window.refresh()

window.getch()
curses.endwin()
