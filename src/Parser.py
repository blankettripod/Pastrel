import Utility
from Token import *
from Error import Error
from Node import Node
from rule import *
from ruleset import *


class Parser:
    def __init__(self, tokens: list[Token], rules: list[Rule]):
        self.tokens = tokens
        self.rules = rules

    def parse(self) -> list[Node]:
        # slr(2) parser

        stack: list = []
        tokenIndex = 0

        while tokenIndex < len(self.tokens):
            stackIndex = 0
            stack.append(self.tokens[tokenIndex])
            tokenIndex += 1

            while stackIndex < len(stack):
                results = self.findAll(stack)
                if results is None:
                    stackIndex += 1
                    continue

                final = results[0]
                for result in results:
                    if result.precedence > final.precedence:
                        final = result
                # this will return the result with the highest precedence
                stack = self.reduce(stack, stackIndex, final)

        return stack

    def findAll(self, stack):
        results = []

        for rule in self.rules:
            results.append(RuleSet.Find(stack, rule))

        output = []
        for result in results:
            if result[0].precedence != -1:
                output.append(result[0])

        if len(output) > 0:
            return output

        return None

    @staticmethod
    def reduce(stack, stackIndex, final) -> list:
        stack = stack[stackIndex+1:]
        stack.append(final)
        return stack



'''
should check all patterns and stack positions for the current stack + 2 more.
all results should be gathered and then the result with highest precedence is chosen
'''

