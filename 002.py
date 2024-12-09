import curses

screen = curses.initscr()

pad = curses.newpad(100, 100)
pad.addstr("This text is thirty characters")

pad.refresh(0, 2, 5, 5, 15, 20)

pad.getch()
curses.endwin()
