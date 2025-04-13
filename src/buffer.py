class Buffer:
    def __init__(self, lines=['']):
        self.lines = lines
    
    def __len__(self):
        return len(self.lines)
    
    def __getitem__(self, index):
        return self.lines[index]

    def __setitem__(self, index, value):
        self.lines[index] = value
    
    def new_line(self):
        self.lines.append('')
    
    def delete_line(self):
        line = self.lines.pop()
        self.lines[-1] += line
    
    def data(self):
        return '\n'.join(self.lines).strip()