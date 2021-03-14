class Token:
    def __init__(self, tpe, value=None):
        self.type = tpe
        self.value = value

    def __repr__(self):
        return f'Token: type = {self.type} {f"value = {self.value}" if self.value is not None else ""}'