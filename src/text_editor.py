import curses
from src.cursor import Cursor
from src.buffer import Buffer


class TextPad:
    def __init__(self, screen):
        self.screen = screen
        self.cursor = Cursor(screen)
        self.buffer = Buffer()

        self.rows, self.cols = self.screen.getmaxyx()
        self.rows -= 1
        self.cols -= 1

        self.offset = 3

        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        
        self.run()

    def display_buffer(self):
        for line_i in range(len(self.buffer)):
            self.screen.addstr(line_i, self.offset, self.buffer[line_i])
    
    def display_extra_suff(self):
        for row in range(0, len(self.buffer)):
            self.screen.addstr(row, 0, str(row+1), curses.color_pair(1) | curses.A_BOLD)

        self.screen.addstr(self.rows, 0, ' -- Insert -- ', curses.A_BOLD)
    
    def update(self):
        self.screen.clear()

        self.display_buffer()
        self.display_extra_suff()
        self.cursor.move(self.offset)

        self.screen.refresh()
    
    def insert(self, ch):
        y, x = self.screen.getyx()
        x -= self.offset

        if x < curses.COLS-1:
            self.buffer[y] = self.buffer[y][:x] + ch + self.buffer[y][x:]
            self.cursor.y, self.cursor.x = y, x+1 
    
    def delete(self):
        y, x = self.screen.getyx()
        x -= self.offset

        if x > 0:
            self.buffer[y] = self.buffer[y][:x-1] + self.buffer[y][x:]
            self.cursor.y, self.cursor.x = y, x-1
        elif x == 0 and y > 0:
            self.buffer.delete_line()
            self.cursor.y, self.cursor.x = y-1, 0
        
    def resize(self):
        self.rows, self.cols = self.screen.getmaxyx()
        self.rows -= 1
        self.cols -= 1

    def run(self):
        while True:
            self.update()
            key = self.screen.getch()

            if key == 27:                          # Escape
                break
             
            if key == 127:                         # Backspace
                self.delete()
            
            elif key == 10:                        # Enter
                self.buffer.new_line()
                self.cursor.y += 1
                self.cursor.x = 0

            elif key == curses.KEY_LEFT:
                self.cursor.left(self.offset)

            elif key == curses.KEY_RIGHT:    
                self.cursor.right(self.offset)
            
            elif key == curses.KEY_RESIZE:
                self.resize()

            else:
                self.insert(chr(key))
