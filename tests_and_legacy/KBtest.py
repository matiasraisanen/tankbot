import curses
import Robot


# Get the curses window, turn off echoing of keyboard to screen, turn on
# instant (no waiting) key response, and use special values for cursor keys
screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)

speed = 255

try:
        while True:
            char = screen.getch()
            if char == ord('q'):
                break
            else:
		print char
finally:
    #Close down curses properly, inc turn echo back on!
 curses.nocbreak(); screen.keypad(0); curses.echo()
 curses.endwin()
 robot.stop()

