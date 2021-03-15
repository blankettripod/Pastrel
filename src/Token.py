class Token:
    def __init__(self, tpe, value=None, start=0, stop = 0):
        self.type = tpe
        self.value = value
        self.start = start
        self.stop = stop

    def __repr__(self):
        return f'Token: type = {self.type} {f"value = {self.value}" if self.value is not None else ""}'