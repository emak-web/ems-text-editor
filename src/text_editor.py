import curses
from src.cursor import Cursor
from src.gap_buffer import Buffer


NORMAL_MODE = 0
INSERT_MODE = 1
COMMAND_MODE = 2


class TextPad:
    def __init__(self, screen, filename):
        self.screen = screen
        self.cursor = Cursor()

        self.rows, self.cols = self.screen.getmaxyx()
        self.rows -= 1
        self.cols -= 1

        self.mode = NORMAL_MODE

        self.offset_left = 3
        self.offset_bottom = 1

        self.buffer = Buffer(filename=filename, rows=self.rows-self.offset_bottom, cols=self.cols-self.offset_left)

        self.command = ''
        self.info_message = ''

        self.running = True

        curses.use_default_colors()

        # Line numbers
        curses.init_color(255, *(int(155*3.92), int(162*3.92), int(224*3.92)))
        curses.init_color(253, *(int(43*3.92), int(43*3.92), int(43*3.92)))
        curses.init_pair(1, 255, 253)

        # Info messages
        curses.init_pair(2, curses.COLOR_GREEN, -1)

        # Default black background 
        # curses.init_color(254, *(0, 0, 0))
        # curses.init_pair(3, -1, 253)
        # self.screen.bkgd(' ', curses.color_pair(3))
        # screen.attrset(curses.color_pair(3))
        
        self.run()

    def display_buffer(self):
        max_line_n = self.buffer.scroll+self.rows-self.offset_bottom+1
        if len(str(max_line_n)) > 3:
            self.offset_left = len(str(max_line_n))+1
        else:
            self.offset_left = 4

        for line_i in range(len(self.buffer)):
            if line_i > self.rows-self.offset_bottom:
                break

            line_n = str(line_i+1+self.buffer.scroll)
            spaces = self.offset_left-len(line_n)-1

            self.screen.addstr(line_i, 0, ' '*spaces+line_n+' ', curses.color_pair(1) | curses.A_BOLD)
            self.screen.addstr(line_i, self.offset_left, self.buffer[line_i][:self.cols-self.offset_left]) # horizontal scroll

    def display_ui(self):
        if self.mode == INSERT_MODE:
            self.screen.addstr(self.rows, 0, '[ Insert Mode ]', curses.A_BOLD)
        elif self.mode == COMMAND_MODE:
            self.screen.addstr(self.rows, 0, '/'+self.command, curses.A_BOLD)
        
        if self.info_message:
            self.screen.addstr(self.rows, 0, self.info_message, curses.color_pair(2))
    
    def display_cursor(self):
        self.screen.move(self.cursor.row, self.cursor.col+self.offset_left)
    
    def update(self):
        self.screen.erase()
        self.display_buffer()
        self.display_ui()
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

        if self.cursor.col + self.offset_left > self.cols:  # Move cursor if needed
            self.cursor.col = self.cols - self.offset_left
        
        if self.cursor.row > self.rows:
            self.cursor.row = self.rows
    
    def normal_mode_handler(self, key):
        if key == 27:                           # Escape
            self.running = False
        
        elif key == 105:                        # i
            self.mode = INSERT_MODE
        
        elif key == 47:                         # /
            self.mode = COMMAND_MODE
        
        elif key == 104:                        # h
            self.buffer.left(self.cursor)
        
        elif key == 108:                        # l
            self.buffer.right(self.cursor)
        
        elif key == 107:                        # k
            self.buffer.up(self.cursor)
        
        elif key == 106:                        # j
            self.buffer.down(self.cursor)
    
    def insert_mode_handler(self, key):
        if key == 27:                           # Escape
            self.mode = NORMAL_MODE
        
        elif key == 127:                        # Backspace
            self.delete()
            
        elif key == 10:                         # Enter
            self.enter()
        
        else:
            self.insert(chr(key))

    def command_mode_handler(self, key):
        if key == 27:                           # Escape
            self.mode = NORMAL_MODE
            self.command = ''
        
        elif key == 10:                         # Enter
            self.execute_command()
            self.mode = NORMAL_MODE
            self.command = ''
        
        elif key == 127:                        # Backspace
            self.command = self.command[:-1]

        else:
            self.command += chr(key)
    
    def execute_command(self):
        if 'w' in self.command:
            self.buffer.save()
            self.info_message = f'Saved to {self.buffer.filename}'
        
        if 'q' in self.command:
            self.running = False

    def run(self):
        while self.running:
            self.update()
            key = self.screen.getch()

            self.info_message = ''

            if key == curses.KEY_LEFT:    
                self.buffer.left(self.cursor)

            elif key == curses.KEY_RIGHT:    
                self.buffer.right(self.cursor)
            
            elif key == curses.KEY_UP:
                self.buffer.up(self.cursor)

            elif key == curses.KEY_DOWN:
                self.buffer.down(self.cursor)
                
            elif key == curses.KEY_RESIZE:
                self.resize()

            elif self.mode == NORMAL_MODE:
                self.normal_mode_handler(key)
            
            elif self.mode == INSERT_MODE:
                self.insert_mode_handler(key)
            
            elif self.mode == COMMAND_MODE:
                self.command_mode_handler(key)