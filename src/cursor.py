class Cursor:
    def __init__(self):
        self.row, self.col = 0, 0
        self.target_col = 0
    
    def left(self):
        self.col -= 1
        self.target_col = self.col

    def right(self):
        self.col += 1
        self.target_col = self.col

    def up(self, buffer):
        self.row -= 1
        self.check_column(buffer)

    def down(self, buffer):
        self.row += 1
        self.check_column(buffer)
    
    def check_column(self, buffer):
        self.col = min(self.target_col, len(buffer[self.row]))
