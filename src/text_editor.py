import curses
import curses.ascii
from src.cursor import Cursor
from src.buffer import Buffer


class TextPad:
    def __init__(self, screen, filename):
        self.screen = screen
        self.cursor = Cursor()

        self.rows, self.cols = self.screen.getmaxyx()
        self.rows -= 1
        self.cols -= 1

        self.buffer = Buffer(filename=filename, rows=self.rows, cols=self.cols)

        self.offset = 3

        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        
        self.run()

    def display_buffer(self):
        for line_i in range(len(self.buffer)):
            if line_i > self.rows:
                break
            self.screen.addstr(line_i, 0, str(line_i+1+self.buffer.scroll), curses.color_pair(1) | curses.A_BOLD)
            self.screen.addstr(line_i, self.offset, self.buffer[line_i][:self.cols-self.offset]) # horizontal scroll
    
    def display_cursor(self):
        self.screen.move(self.cursor.row, self.cursor.col+self.offset)
    
    def update(self):
        self.screen.erase()
        self.display_buffer()
        self.display_cursor()
        self.screen.refresh()
    
    def insert(self, ch):
        self.buffer.insert_ch(ch, self.cursor)
    
    def delete(self):
        if self.cursor.col > 0:
            self.buffer.delete_ch(self.cursor)

        elif self.cursor.row+self.buffer.scroll > 0:
            self.buffer.delete_line(self.cursor)

    def enter(self):
        self.buffer.insert_line(self.cursor)
        
    def resize(self):
        self.rows, self.cols = self.screen.getmaxyx()
        self.rows -= 1
        self.cols -= 1
        self.buffer.rows, self.buffer.cols = self.rows, self.cols

        if self.cursor.col + self.offset > self.cols:
            self.cursor.col = self.cols - self.offset
        
        if self.cursor.row > self.rows:
            self.cursor.row = self.rows

    def run(self):
        while True:
            self.update()
            key = self.screen.getch()

            if key == 27:                          # Escape
                break
                
            elif key == curses.ascii.ETB:          # CTRL+W
                self.buffer.save()
             
            elif key == 127:                       # Backspace
                self.delete()
            
            elif key == 10:                        # Enter
                self.enter()

            elif key == curses.KEY_LEFT:
                if self.cursor.col > 0:
                    self.cursor.left()

            elif key == curses.KEY_RIGHT:
                if self.cursor.col < self.cols-self.offset and self.cursor.col < len(self.buffer[self.cursor.row]):
                    self.cursor.right()
            
            elif key == curses.KEY_UP:
                self.buffer.up(self.cursor)

            elif key == curses.KEY_DOWN:
                self.buffer.down(self.cursor)
                
            elif key == curses.KEY_RESIZE:
                self.resize()

            else:
                self.insert(chr(key))
