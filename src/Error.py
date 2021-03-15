class Error:
    def __init__(self, message, line, startx=0, endx=0, text='\n'):
        self.message = message
        self.line = line
        self.startx = startx
        self.endx = endx
        self.text = text

    def Assert(self):
        line = str(self.text).splitlines()[self.line]
        return f"Error: on line {self.line} - {self.message}\n" \
               f"{line}\n" \
               f"{' '*self.startx}^{'~'*(self.endx-self.startx)}" 

    def __repr__(self):
        return self.Assert()