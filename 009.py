import curses

screen = curses.initscr()

maxy, maxx = screen.getmaxyx()

input_window = curses.newwin(3, maxx)
text_window = curses.newwin(maxy - 4, maxx, 3, 0)
input_window.box()
text_window.box()
input_window.refresh()
text_window.refresh()
input_window.move(1, 1)
input = input_window.getstr()
text_window.move(1, 1)
text_window.addstr(input.decode("utf-8"))
text_window.getch()


curses.endwin()
