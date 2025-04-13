import curses
from src.text_editor import TextPad


def main(screen):
    text_editor = TextPad(screen)
    

if __name__ == '__main__':
    curses.wrapper(main)