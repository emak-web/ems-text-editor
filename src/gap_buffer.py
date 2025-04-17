class Line:
    def __init__(self, value=[], default_gap_size=16, prev=None, next=None):
        self.default_gap_size = default_gap_size
        self.gap_size = 0
        self.gap_i = 0
        self.value = value
        self.prev = prev
        self.next = next
    
    def repr(self):
        line = ''
        for ch in self.value:
            if ch:
                line += ch
            # For debug
            # else:
            #     line += '_'
        
        return line

    def move(self, index):
        if index > self.gap_i:
            for _ in range(index-self.gap_i):
                self.right()
        elif index < self.gap_i:
            for _ in range(self.gap_i-index):
                self.left()

    def insert(self, ch):
        if self.gap_size == 0:
            for _ in range(self.default_gap_size):
                self.value.insert(self.gap_i, None)
            self.gap_size = self.default_gap_size

        self.value[self.gap_i] = ch
        self.gap_i += 1
        self.gap_size -= 1
    
    def remove(self):
        if self.gap_i > 0:
            self.gap_i -= 1
            self.value[self.gap_i] = None
            self.gap_size += 1

    def left(self):
        if self.gap_i > 0:
            self.gap_i -= 1
            if self.gap_size > 0:
                self.value[self.gap_i+self.gap_size] = self.value[self.gap_i]
                self.value[self.gap_i] = None
    
    def right(self):
        if self.gap_i < len(self.value) - self.gap_size:
            if self.gap_size > 0:
                self.value[self.gap_i] = self.value[self.gap_i+self.gap_size]
                self.value[self.gap_i+self.gap_size] = None
            self.gap_i += 1


class Buffer:
    def __init__(self, filename, rows=0, cols=0):
        self.filename = filename
        self.rows = rows
        self.cols = cols
        self.scroll = 0

        self.load()
    
    def __len__(self):
        cur = self.first_line
        length = 0

        while cur:
            length += 1
            cur = cur.next
        
        return length
    
    def __getitem__(self, index):
        cur = self.first_line

        for _ in range(index):
            cur = cur.next
        
        return cur.repr()
    
    def load(self):
        res = Line()
        if self.filename:
            try:
                cur = res
                with open(self.filename) as file:
                    for line in file:
                        cur.next = Line(value=list(line.rstrip()))
                        prev = cur
                        cur = cur.next
                        cur.prev = prev
                if res.next:
                    self.lines = res.next
                else:
                    self.lines = res
            except FileNotFoundError:
                self.lines = res
        else:
            self.lines = res

        self.lines.prev = None
        self.first_line = self.lines
        self.current_line = self.lines
    
    def save(self):
        if self.filename:
            with open(self.filename, '+w') as file:
                cur = self.lines
                while cur:
                    file.write(cur.repr()+'\n')
                    cur = cur.next
    
    def left(self, cursor):
        self.current_line.left()
        cursor.left()

    def right(self, cursor):
        self.current_line.right()
        cursor.right(self)
           
    def up(self, cursor):
        if self.current_line.prev:
            self.current_line = self.current_line.prev

            if cursor.row > 0:
                cursor.up(self)

            elif self.scroll > 0:
                self.scroll -= 1
                self.first_line = self.first_line.prev
                cursor.check_column(self)

            self.current_line.move(cursor.col)

    def down(self, cursor):
        if self.current_line.next:
            self.current_line = self.current_line.next

            if cursor.row < self.rows:  
                cursor.down(self)

            elif cursor.row == self.rows:
                self.scroll += 1
                self.first_line = self.first_line.next
                cursor.check_column(self)
            
        elif cursor.row > 0:
            self.scroll += 1
            self.first_line = self.first_line.next
            cursor.row -= 1
            
        self.current_line.move(cursor.col)
    
    def insert_ch(self, ch, cursor):
        self.current_line.insert(ch)
        cursor.right(self)
    
    def insert_line(self, cursor):
        new_line = self.current_line.value[self.current_line.gap_i+self.current_line.gap_size:]
        self.current_line.value = self.current_line.value[:self.current_line.gap_i+self.current_line.gap_size]

        if cursor.row == self.rows:
            self.scroll += 1
            self.first_line = self.first_line.next
        else:
            cursor.row += 1 
            
        cursor.col = 0
        cursor.target_col = cursor.col

        prev = self.current_line
        next = self.current_line.next
        self.current_line.next = Line(value=new_line)
        self.current_line = self.current_line.next
        self.current_line.prev = prev
        self.current_line.next = next

        if next:
            next.prev = self.current_line

    def delete_ch(self, cursor):
        self.current_line.remove()
        cursor.left()

    def delete_line(self, cursor):
        current_line = self.current_line.value[self.current_line.gap_i+self.current_line.gap_size:]

        if cursor.row == 0:
            self.scroll -= 1
            self.first_line = self.first_line.prev
        else:
            cursor.up(self)
        
        next_line = self.current_line.next
        self.current_line = self.current_line.prev
        self.current_line.next = next_line

        if next_line:
            next_line.prev = self.current_line

        cursor.col = len(self.current_line.value)-self.current_line.gap_size
        cursor.target_col = cursor.col

        self.current_line.move(len(self.current_line.value))
        self.current_line.value += current_line
        