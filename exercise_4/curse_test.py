import curses
stdscr = curses.initscr()
curses.start_color()
# Must be called for use colors and before any other color manipulation routine is called.
curses.curs_set(0)
stdscr.addstr("Regular\n")
stdscr.addstr("Bold\n", curses.A_BOLD)
stdscr.addstr("Highlighted\n", curses.A_STANDOUT)
stdscr.addstr("Underline\n", curses.A_UNDERLINE)
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
stdscr.addstr("RED ALERT!\n", curses.color_pair(1))
stdscr.addstr("SUPER RED ALERT!\n", curses.color_pair(1) | curses.A_BOLD | curses.A_UNDERLINE | curses.A_BLINK)

stdscr.addstr("Hey", curses.color_pair(1))
stdscr.refresh()
curses.napms(10000)
curses.endwin()