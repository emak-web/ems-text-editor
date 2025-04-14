import curses
import sys
from src.text_editor import TextPad


def main(screen):
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = None

    TextPad(screen, filename)


if __name__ == '__main__':
    curses.wrapper(main)
