from typing import Union

from Token import Token as token
from Node import *

from rule import Rule


class RuleSet:
    @staticmethod
    def Find(pattern: list[token], rule=None, patternI=0, lookahead="") -> list[Node, int]:
        patternIndex = patternI
        ruleIndex = 0
        output = []
        passes = 0

        while ruleIndex < len(rule.parts) and patternIndex < len(pattern):
            if isinstance(rule.parts[ruleIndex], Rule):  # standard rule
                start = patternIndex
                result, patternIndex = RuleSet.Find(pattern, rule.parts[ruleIndex], patternIndex)
                patternIndex += 1
                if result.type != "none":  # rule matched pattern
                    output.append(result)
                    passes += 1
                else:
                    patternIndex = start

            elif isinstance(rule.parts[ruleIndex], tuple):  # option rule
                for option in rule.parts[ruleIndex]:
                    start = patternIndex
                    result, patternIndex = RuleSet.Find(pattern, option, patternIndex)
                    patternIndex += 1
                    if result.type != "none":  # rule matched pattern
                        output.append(result)
                        passes += 1
                        break
                    else:
                        patternIndex = start

            elif isinstance(rule.parts[ruleIndex], list):  # repetition rule
                repeatOutput: list[list[Node]] = []
                start = patternIndex
                while True:
                    subOutput: list[Node] = []
                    subPasses = 0
                    for subRule in rule.parts[ruleIndex]:
                        result, patternIndex = RuleSet.Find(pattern, subRule, patternIndex)
                        patternIndex += 1
                        if result.type != "none":  # rule matched pattern
                            subOutput.append(result)
                            subPasses += 1
                            break
                    if subPasses == len(rule.parts[ruleIndex]):  # were all the rules fulfilled completely
                        repeatOutput.append(subOutput)
                    else:
                        break
                if len(repeatOutput) > 0:
                    passes += 1
                    output.append(Node(rule.parts[ruleIndex].identifier))

            elif isinstance(rule.parts[ruleIndex], set):  # literal rule
                if isinstance(pattern[patternIndex], token) and pattern[patternIndex].value in rule.parts[ruleIndex]:
                    passes += 1
                    output.append(Node("literal", pattern[patternIndex].value))

            elif isinstance(rule.parts[ruleIndex], str):  # type rule
                if pattern[patternIndex].type == rule.parts[ruleIndex]:
                    passes += 1
                    output.append(Node(pattern[patternIndex].type, pattern[patternIndex].value))

            else:
                raise SystemExit(f"Invalid rule type on rule {rule}\n{type(rule)}")
            patternIndex += 1
            ruleIndex += 1

        if passes == len(rule.parts):
            print(f"found {rule.identifier} node")
            return [Node(rule.identifier, output, rule.precedence), patternIndex-1]

        return [Node("none"), patternIndex-1]
