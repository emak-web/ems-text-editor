import curses
from src.text_editor import TextEditor


def main(screen):
    text_editor = TextEditor(screen)
    

if __name__ == '__main__':
    curses.wrapper(main)