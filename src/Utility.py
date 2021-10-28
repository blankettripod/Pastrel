def LineFromCode(code: str = "", line: int = 0):
    ln = 0
    output = ""
    for character in code:
        if character == '\n':
            ln += 1
            continue

        if ln == line:
            output += character

    return output


def PointOnLine(code: str, line: int, x: int):
    i = 0
    current_line = 0

    while i < len(code):
        if current_line == line:
            return i + x
        i += 1


def ParseArguments(argv: list[str]) -> list:
    output = {}

    i = 0
    while i < len(argv):
        if argv[i].startswith('-'):
            if i + 1 < len(argv):
                if argv[i + 1].startswith('-'):
                    output[argv[i]] = ''

                else:
                    output[argv[i]] = argv[i + 1]
                    i += 2
                    continue
            else:
                output[argv[i]] = argv[i + 1]
                i += 2
                continue
        else:
            output[argv[i]] = ''
        i += 1
    output = list(output.items())
    return output
