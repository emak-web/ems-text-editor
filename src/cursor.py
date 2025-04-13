class Cursor:
    def __init__(self):
        self.row, self.col = 0, 0
        self.target_col = 0
    
    def left(self):
        self.col -= 1

    def right(self):
        self.col += 1

    def up(self, buffer):
        self.row -= 1
        self.col = min(self.col, len(buffer[self.row]))

    def down(self, buffer):
        self.row += 1
        self.col = min(self.col, len(buffer[self.row]))
