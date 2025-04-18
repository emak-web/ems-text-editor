class Buffer:
    def __init__(self, filename, rows=0, cols=0):
        self.lines = []
        self.filename = filename
        self.rows = rows
        self.cols = cols
        self.scroll = 0

        self.load()
    
    def __len__(self):
        return len(self.lines)-self.scroll
    
    def __getitem__(self, index):
        return self.lines[index+self.scroll]

    def __setitem__(self, index, value):
        self.lines[index+self.scroll] = value
    
    def __bool__(self):
        if self.lines != ['']:
            return True
        else:
            return False
    
    def load(self):
        if self.filename:
            try:
                with open(self.filename) as file:
                    for line in file:
                        self.lines.append(line.rstrip())
            except FileNotFoundError:
                self.lines = ['']
        else:
            self.lines = ['']
    
    def save(self):
        if self.filename:
            with open(self.filename, '+w') as file:
                for line in self.lines:
                    file.write(line+'\n')
    
    def left(self, cursor):
        cursor.left()

    def right(self, cursor):
        cursor.right(self)
                    
    def up(self, cursor):
        if cursor.row > 0:
            cursor.up(self)

        elif self.scroll > 0:
            self.scroll -= 1
            cursor.check_column(self)

    def down(self, cursor):
        if cursor.row < self.rows and cursor.row < len(self)-1:  
            cursor.down(self)

        elif cursor.row == self.rows and cursor.row < len(self)-1:
            self.scroll += 1
            cursor.check_column(self)
        
        elif cursor.row > 0:
            self.scroll += 1
            cursor.row -= 1
    
    def pop(self, index=-1):
        return self.lines.pop(index+self.scroll)
    
    def insert(self, index, value):
        self.lines.insert(index+self.scroll, value)
    
    def insert_ch(self, ch, cursor):
        self[cursor.row] = self[cursor.row][:cursor.col] + ch + self[cursor.row][cursor.col:]
        cursor.right(self)
    
    def insert_line(self, cursor):
        new_line = self[cursor.row][cursor.col:]
        self[cursor.row] = self[cursor.row][:cursor.col]

        if cursor.row == self.rows:
            self.scroll += 1
        else:
            cursor.row += 1 
            
        cursor.col = 0
        cursor.target_col = cursor.col
        self.insert(cursor.row, new_line)
    
    def delete_ch(self, cursor):
        self[cursor.row] = self[cursor.row][:cursor.col-1] + self[cursor.row][cursor.col:]
        cursor.left()

    def delete_line(self, cursor):
        current_line = self.pop(cursor.row)

        if cursor.row == 0:
            self.scroll -= 1
        else:
            cursor.up(self)

        cursor.col = len(self[cursor.row])
        cursor.target_col = cursor.col
        self[cursor.row] += current_line