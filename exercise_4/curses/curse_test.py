import curses
import datetime
import time



stdscr = curses.initscr()
def show_textc(t): stdscr.addstr(f"{datetime.datetime.now()} {t}") 
# Must be called for use colors and before any other color manipulation routine is called.
curses.start_color()
#   curs_set change the set cursos state, in this case invisible.
curses.curs_set(0)
#   addrstr to write strings
curses.init_pair(5,4,0)
stdscr.addstr("test color", curses.color_pair(5))

stdscr.addstr("Regular\n")
stdscr.addstr("Bold\n", curses.A_BOLD)
stdscr.addstr("Highlighted\n", curses.A_STANDOUT)
stdscr.addstr("Underline\n", curses.A_UNDERLINE)
#   init_pair uses to change color of strings
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
#   to change color need be called in the end of the string, and the number "1" is the init_pair index
stdscr.addstr("RED ALERT!\n", curses.color_pair(1))
#   to add more aspects
stdscr.addstr("SUPER RED ALERT!\n", curses.color_pair(1) | curses.A_BOLD | curses.A_UNDERLINE | curses.A_BLINK)
curses.init_pair(3, 1, 0)
#    test with other color
curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_MAGENTA)
stdscr.addstr("Hey", curses.color_pair(3))
#   if the text dont have any specification it get the system color/...
stdscr.addstr("this is a test\n")
#   test with input
nonstop = True
nickname = ""
while nonstop:
    letter = stdscr.getch()
    nickname += chr(letter)
    if letter == 10:
        show_textc(nickname)
        nonstop = False

#   sincronize the actual screen with previus methods/deleted
stdscr.refresh()
#   seconds until close
stdscr.addstr("Hey")
time.sleep(10)
stdscr.refresh()
time.sleep(10)
#   close program
curses.endwin()