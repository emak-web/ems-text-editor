import curses


class Cursor:
    def __init__(self, screen):
        self.screen = screen
        self.y, self.x = screen.getyx()
    
    def move(self, gap_x):
        self.screen.move(self.y, self.x+gap_x)
    
    def left(self, gap_x):
        y, x = self.screen.getyx()
        x -= gap_x

        if x-1 >= 0:
            self.y, self.x = y, x-1

    def right(self, gap_x):
        y, x = self.screen.getyx()
        x -= gap_x

        if x < curses.COLS-1:
            self.y, self.x = y, x+1
