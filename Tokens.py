class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __str__(self):
        return f"|{self.type}{(': ' + str(self.value)) if self.value is not None else ''}|"

    def __repr__(self):
        return f"|{self.type}{(': ' + str(self.value)) if self.value is not None else ''}|"


