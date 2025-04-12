import curses


class Cursor:
    def __init__(self, screen):
        self.screen = screen
        self.y, self.x = screen.getyx()
    
    def move(self):
        self.screen.move(self.y, self.x)
    
    def move_left(self):
        y, x = self.screen.getyx()
        if x-1 >= 0:
            self.y, self.x = y, x-1

    def move_right(self):
        y, x = self.screen.getyx()
        if x < curses.COLS-1:
            self.y, self.x = y, x+1
