import curses
from src.cursor import Cursor


class TextEditor:
    def __init__(self, screen):
        self.screen = screen
        self.cursor = Cursor(screen)
        self.data = ''
        self.run()
    
    def update(self):
        self.screen.clear()
        self.screen.addstr(self.data)
        self.cursor.move()
        self.screen.refresh()
    
    def insert(self, ch):
        y, x = self.screen.getyx()
        if x < curses.COLS-1:
            self.data = self.data[:x] + ch + self.data[x:]
            self.cursor.y, self.cursor.x = y, x+1 
    
    def delete(self):
        y, x = self.screen.getyx()

        if x > 0 and x <= len(self.data):
            self.data = self.data[:x-1] + self.data[x:]
            self.cursor.y, self.cursor.x = y, x-1
    
    def run(self):
        self.screen.clear()
        self.screen.addstr(self.data)

        while True:
            key = self.screen.getch()

            # Escape
            if key == 27:
                break
             
            # Backspace
            if key == 127:
                self.delete()

            elif key == curses.KEY_LEFT:
                self.cursor.move_left()

            elif key == curses.KEY_RIGHT:
                self.cursor.move_right()

            else:
                self.insert(chr(key))

            self.update()
