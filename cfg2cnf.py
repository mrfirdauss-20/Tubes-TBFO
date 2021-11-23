# File      : cfg2cnf.py
# Author    : Hilya Fadhilah Imania
# Created   : 2021/11/21
# Version   : 0.0.2
import codecs
from typing import TypeVar

S = TypeVar("S")


class Cfg2Cnf:
    prods: dict[list[str]] = {}
    terminals: list[str] = []
    variables: list[str] = []
    start_sym: str

    def __init__(self, filename: str, start_sym: str) -> None:
        state = None
        with codecs.open(filename, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line == "Terminals:":
                    state = "T"
                elif line == "Variables:":
                    state = "V"
                elif line == "Productions:":
                    state = "P"
                elif state == "T":
                    self.__extend_unique(self.terminals, line.split())
                elif state == "V":
                    self.__extend_unique(self.variables, line.split())
                elif state == "P":
                    if "->" in line:
                        lhs, rhs = line.split("->", maxsplit=2)
                        sym = lhs.strip()
                        rules = [rule.split() for rule in rhs.split("|")]
                        self.prods[sym] = rules

        self.start_sym = start_sym

    def is_terminal(self, sym) -> bool:
        return sym in self.terminals

    def convert(self) -> None:

        # step 1: eliminate start symbol from RHS

        try:
            for rule in self.prods[self.start_sym]:
                if self.start_sym in rule:
                    new_sym = f"{self.start_sym}0"
                    new_prods = {new_sym: [[self.start_sym]]}
                    new_prods.update(self.prods)
                    self.prods = new_prods
                    self.start_sym = new_sym
                    self.variables.insert(0, new_sym)
                    raise
        except:
            pass

        # step 2a: remove null productions

        null_prods = []
        for sym in self.prods:
            if ["ε"] in self.prods[sym]:
                null_prods.append(sym)

        while null_prods:
            sym = null_prods.pop(0)
            self.prods[sym].remove(["ε"])

            # replace for this production first

            for rule in self.prods[sym]:
                self.__extend_unique(
                    self.prods[sym], self.__replace_nullable(rule, sym)
                )

            # replace for other productions

            for other in self.prods:
                if other != sym:
                    for rule in self.prods[other]:
                        self.__extend_unique(
                            self.prods[other], self.__replace_nullable(rule, sym)
                        )
                    if ["ε"] in self.prods[other]:
                        null_prods.insert(0, other)

        # step 2b: remove unit productions

        unit_prods = []
        for sym in self.prods:
            for rule in self.prods[sym]:
                if len(rule) == 1 and not self.is_terminal(rule[0]):
                    unit_prods.append((sym, rule[0]))

        while unit_prods:
            sym, unit_sym = unit_prods.pop()
            if unit_sym in self.prods:
                self.prods[sym].remove([unit_sym])
                if unit_sym != sym:
                    for rule in self.prods[unit_sym]:
                        if len(rule) > 1 or self.is_terminal(rule[0]):
                            self.__extend_unique(self.prods[sym], [rule])
                        else:
                            unit_prods.append([sym, rule[0]])

        # step 2c: remove useless productions

        self.__remove_useless()

        # step 3: decompose terminals

        new_prods = {}
        for sym in self.prods:
            counter = 1
            new_terms = {}
            for rule in self.prods[sym]:
                terms, vrbls = self.__split_rule(rule)
                if (terms and vrbls) or (len(terms) > 1):
                    for i in range(len(rule)):
                        if self.is_terminal(rule[i]):
                            if rule[i] in new_terms:
                                new_sym = new_terms[rule[i]]
                            else:
                                new_sym = f"{sym}_T{counter}"
                                new_terms[rule[i]] = new_sym
                                self.variables.append(new_sym)
                                counter += 1
                            rule[i] = new_sym

            for term, new_sym in new_terms.items():
                new_prods[new_sym] = [[term]]

            # step 4: decompose symbols

            plus_prods = []
            for rule in self.prods[sym]:
                if len(rule) > 2:
                    plus_prods.append(rule)

            counter = 1
            while plus_prods:
                rule = plus_prods.pop()
                plus_prod = rule[1:]

                new_sym = f"{sym}_S{counter}"
                new_prods[new_sym] = [plus_prod]
                counter += 1

                del rule[1:]
                rule.append(new_sym)
                self.variables.append(new_sym)

                if len(plus_prod) > 2:
                    plus_prods.append(plus_prod)

        self.prods.update(new_prods)

    def write(self, filename: str, complete: bool = False) -> None:
        with codecs.open(filename, mode="w", encoding="utf-8") as f:
            if complete:
                f.write("Terminals:\n")
                f.write(" ".join(self.terminals))
                f.write("\nVariables:\n")
                f.write(" ".join(self.variables))
                f.write("\nProductions:\n")
            for sym, rules in self.prods.items():
                prods_str = map(lambda p: " ".join(p), rules)
                f.write(f"{sym} -> {' | '.join(prods_str)}\n")

    def __split_rule(self, rule: list[str]) -> tuple[list[str], list[str]]:
        terms = []
        vrbls = []
        for sym in rule:
            if self.is_terminal(sym):
                terms.append(sym)
            else:
                vrbls.append(sym)
        return terms, vrbls

    def __replace_nullable(
        self, prod: list[str], null_sym: str, start: int = 0
    ) -> list[str]:
        result = []
        length = len(prod)

        for i in range(start, length):
            if prod[i] == null_sym:
                new_rule = prod[:i] + prod[i + 1 :]

                if len(new_rule) == 0:
                    self.__append_unique(result, ["ε"])
                else:
                    self.__append_unique(result, new_rule)

                rec = self.__replace_nullable(new_rule, null_sym, i)
                for new_rule in rec:
                    self.__append_unique(result, new_rule)

        return result

    def __remove_useless(self) -> None:

        # traverse from start symbol, obtain stack

        terms = []
        vrbls = [self.start_sym]
        self.__traverse(self.start_sym, terms, vrbls)

        # delete items not in stack (unreachable)

        dels = []
        for sym in self.prods:
            if sym not in vrbls:
                dels.append(sym)
            for rule in self.prods[sym]:
                for rule_sym in rule:
                    if self.is_terminal(rule_sym) and rule_sym not in terms:
                        dels.append(rule_sym)

        for sym in self.terminals:
            if sym not in terms:
                dels.append(sym)

        for sym in self.variables:
            if sym not in vrbls:
                dels.append(sym)

        self.__delete_rules(dels)

        # unterminable productions:
        # initialize obviously terminable productions

        terminables = []
        unterminables = []
        for sym in self.prods:
            can_terminate = False
            for rule in self.prods[sym]:
                _, vrbls = self.__split_rule(rule)
                if not vrbls:
                    can_terminate = True
                    break
            if can_terminate:
                terminables.append(sym)
            else:
                unterminables.append(sym)

        # unterminable might be actually terminable, check
        # using "queue", unterminable goes back to the end of line
        # until it's indefinitely repeating

        stack = []
        while unterminables:
            sym = unterminables.pop()
            can_terminate = False
            for rule in self.prods[sym]:
                for rule_sym in rule:
                    if rule_sym in terminables:
                        can_terminate = True
                        break
                if can_terminate:
                    break

            if can_terminate:
                terminables.append(sym)
            else:
                unterminables.insert(0, sym)
                stack.append(sym)

            if self.__is_repeating(stack):
                break

        self.__delete_rules(unterminables)

    def __delete_rules(self, syms: list[str]) -> None:

        # delete rules

        for sym in self.prods:
            rules = []
            for rule in self.prods[sym]:
                can_terminate = True
                for rule_sym in rule:
                    if rule_sym in syms:
                        can_terminate = False
                        break
                if can_terminate:
                    rules.append(rule)
            self.prods[sym] = rules

        # delete productions

        for sym in syms:
            if sym in self.prods:
                del self.prods[sym]
            if sym in self.variables:
                self.variables.remove(sym)
            elif sym in self.terminals:
                self.terminals.remove(sym)

    def __traverse(self, sym: str, terms: list[str], vrbls: list[str]) -> None:
        for rule in self.prods[sym]:
            for rule_sym in rule:
                if (
                    self.is_terminal(rule_sym)
                    and rule_sym not in terms
                    and rule_sym in self.terminals
                ):
                    terms.append(rule_sym)
                elif (
                    not self.is_terminal(rule_sym)
                    and rule_sym not in vrbls
                    and rule_sym in self.variables
                ):
                    vrbls.append(rule_sym)
                    self.__traverse(rule_sym, terms, vrbls)

    def __extend_unique(self, lst: list[S], ext: list[S]) -> None:
        for val in ext:
            if val not in lst:
                lst.append(val)

    def __append_unique(self, lst: list[S], val: S) -> None:
        if val not in lst:
            lst.append(val)

    def __is_repeating(self, visited: list[S]) -> bool:
        unrepeated = []
        for i in range(len(visited)):
            try:
                j = -1
                while True:
                    j = unrepeated.index(visited[i], j + 1)
                    if visited[i + 1] == unrepeated[j + 1]:
                        return True
            except:
                pass
            unrepeated.append(visited[i])
        return False


if __name__ == "__main__":
    import argparse
    import time

    parser = argparse.ArgumentParser()
    parser.add_argument("infile")
    parser.add_argument("outfile")
    parser.add_argument("start_symbol")
    parser.add_argument("--complete", action=argparse.BooleanOptionalAction)

    args = parser.parse_args()
    t1 = time.perf_counter()

    converter = Cfg2Cnf(args.infile, args.start_symbol)
    converter.convert()
    converter.write(args.outfile, args.complete)

    t2 = time.perf_counter()
    print(f"Done in {t2 - t1}s", end="\n\n")
