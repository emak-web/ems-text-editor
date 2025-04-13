class Buffer:
    def __init__(self, lines=['']):
        self.lines = lines
    
    def __len__(self):
        return len(self.lines)
    
    def __getitem__(self, index):
        return self.lines[index]

    def __setitem__(self, index, value):
        self.lines[index] = value
    
    def pop(self, index=-1):
        return self.lines.pop(index)
    
    def insert(self, index, value):
        self.lines.insert(index, value)
