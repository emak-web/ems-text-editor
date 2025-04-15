import curses
import sys
import os
from src.text_editor import TextPad


def main(screen):
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = None

    # os.environ.setdefault('ESCDELAY', '25')
    curses.set_escdelay(25)

    TextPad(screen, filename)


if __name__ == '__main__':
    curses.wrapper(main)
