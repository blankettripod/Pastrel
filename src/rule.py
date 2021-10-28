#  a tuple in a rule means OR e.g. term -> [factor, ('+', '-', '*', '/'), factor]
#  a list in a rule means repeat e.g. term ->
#
from typing import Union

import Token


class Rule:
    identifier: str = ''
    parts = []
    precedence: int = 0

    def __init__(self, identifier="", parts=(), precedence=0):
        self.identifier = identifier
        self.parts: list[Union[Rule, list, tuple, set, str]] = parts
        self.precedence = precedence

    def __repr__(self):
        return f"rule: {self.identifier}"

