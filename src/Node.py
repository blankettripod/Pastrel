import Token


class Node:
    type: str = "uk"
    value = [None]

    def __init__(self, nType, value=None, precedence=-1):
        self.type = nType
        self.value = value
        self.precedence = precedence

    def display(self, indents=0):
        start = f"\n{'    ' * indents}{self.type} Node ["
        middle = f""
        end = f"\n{'    ' * indents}]"

        if isinstance(self.value, Node):
            middle += self.value.display(indents)

        elif isinstance(self.value, list):
            for value in self.value:
                middle += value.display(indents+1)

        elif isinstance(self.value, Token.Token):
            middle += f'\n{"    " * indents}' + self.value.__repr__()

        elif isinstance(self.value, str):
            middle += f'\n{"    " * (indents+1)}' + self.value

        elif isinstance(self.value, int):
            middle += f'\n{"    " * (indents+1)}' + str(self.value)

        elif isinstance(self.value, float):
            middle += f'\n{"    " * (indents+1)}' + str(self.value)

        return start + middle + end

    def __repr__(self):
        return self.display()
