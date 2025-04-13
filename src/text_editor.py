import curses
from src.cursor import Cursor
from src.buffer import Buffer


class TextPad:
    def __init__(self, screen):
        self.screen = screen
        self.cursor = Cursor()
        self.buffer = Buffer(['LINE 1', 'This is line 2', 'I am line 3!', ':) line 4'])

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
        for row in range(len(self.buffer)):
            self.screen.addstr(row, 0, str(row+1), curses.color_pair(1) | curses.A_BOLD)

        self.screen.addstr(self.rows, 0, ' -- Insert -- ', curses.A_BOLD)
    
    def display_cursor(self):
        self.screen.move(self.cursor.row, self.cursor.col+self.offset)
    
    def update(self):
        self.screen.clear()
        self.display_buffer()
        self.display_extra_suff()
        self.display_cursor()
        self.screen.refresh()
    
    def insert(self, ch):
        self.buffer[self.cursor.row] = self.buffer[self.cursor.row][:self.cursor.col] + ch + self.buffer[self.cursor.row][self.cursor.col:]
        self.cursor.right()
    
    def delete(self):
        if self.cursor.col > 0:
            self.buffer[self.cursor.row] = self.buffer[self.cursor.row][:self.cursor.col-1] + self.buffer[self.cursor.row][self.cursor.col:]
            self.cursor.left()

        elif self.cursor.row > 0:
            current_line = self.buffer.pop(self.cursor.row)
            self.cursor.row -= 1
            self.cursor.col = len(self.buffer[self.cursor.row])
            self.buffer[self.cursor.row] += current_line

    def enter(self):
        new_line = self.buffer[self.cursor.row][self.cursor.col:]
        self.buffer[self.cursor.row] = self.buffer[self.cursor.row][:self.cursor.col]
        self.cursor.row += 1
        self.cursor.col = 0
        self.buffer.insert(self.cursor.row, new_line)
        
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
                self.enter()

            elif key == curses.KEY_LEFT:
                if self.cursor.col > 0:
                    self.cursor.left()

            elif key == curses.KEY_RIGHT:
                if self.cursor.col < self.cols-self.offset and self.cursor.col < len(self.buffer[self.cursor.row]):
                    self.cursor.right()
            
            elif key == curses.KEY_UP:
                if self.cursor.row > 0: 
                    self.cursor.up(self.buffer)

            elif key == curses.KEY_DOWN:
                if self.cursor.row < self.rows and self.cursor.row < len(self.buffer)-1:  
                    self.cursor.down(self.buffer)
                
            elif key == curses.KEY_RESIZE:
                self.resize()

            else:
                self.insert(chr(key))
