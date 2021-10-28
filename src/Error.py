class Error:

    def __init__(self, code: str="E0000", message: str="Error", line: int=0, startX: int=0, endX: int=0, lCode: str="") -> None:
        self.code = code
        self.message = message
        self.line = line
        self.startX = startX
        self.endX = endX
        self.lCode = lCode

    def Assert(self) -> str:
        return f"Error {self.code} at {self.startX}:{self.endX} -> {self.message}\n" \
            f"{self.lCode}\n" \
            f"{' ' * self.startX}^{'~' * (self.endX-self.startX-1)}\n"

