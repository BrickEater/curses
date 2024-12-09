import curses

screen = curses.initscr()
main_window = curses.newwin(40, 40)
main_window.box()
main_window.move(1, 1)
main_window.getstr()
main_window.getch()
curses.endwin()
