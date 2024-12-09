import curses

screen = curses.initscr()
maxy, maxx = screen.getmaxyx()
curses.curs_set(0)

window = curses.newwin(11, maxx, 10, 0)
window.border()
window.refresh()

input_box1 = curses.newwin(3, maxx // 2, 11, maxx // 2 - 1)
input_box1.border()
input_box1.addstr(0, 1, " Category ")
input_box1.refresh()

input_box2 = curses.newwin(3, maxx // 2, 14, maxx // 2 - 1)
input_box2.border()
input_box2.addstr(0, 1, " Item ")
input_box2.refresh()

input_box3 = curses.newwin(3, maxx // 2, 17, maxx // 2 - 1)
input_box3.border()
input_box3.addstr(0, 1, " Value ")
input_box3.refresh()

input_box1.getch()

curses.endwin()
