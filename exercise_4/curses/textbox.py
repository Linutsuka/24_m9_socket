import curses
from curses.textpad import Textbox, rectangle

def main(stdscr):
    stdscr.addstr(0, 0, "Enter IM message: (hit Ctrl-G to send)")

    editwin = curses.newwin(5,30, 2,1)
    rectangle(stdscr, 1,0, 1+5+1, 1+30+1)
    stdscr.refresh()

    box = Textbox(editwin)
    # Let the user edit until Ctrl-G is struck.
    box.edit()

    # Get resulting contents
    message = box.gather()


stdscr = curses.initscr()
# Must be called for use colors and before any other color manipulation routine is called.
curses.start_color()
#   curs_set change the set cursos state, in this case invisible.
curses.curs_set(0)
#   addrstr to write strings
stdscr.addstr("start")
#   init_pair uses to change color of strings
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
rext = main(stdscr)
stdscr.addstr(rext)
stdscr.refresh()
#   seconds until close
curses.napms(10000)
#   close program
curses.endwin()