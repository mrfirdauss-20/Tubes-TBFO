#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Convert Context-Free Grammar (CFG) to Chomsky Normal Form (CFG)

Notes
-----
This file can be used as a script or as a package. The script section
also serves as the class usage example.

Important:
    S -> ε (empty string) is assumed to be valid by default.
    If there is a requirement to handle this differently,
    do not use the script directly.

Usage
-----
    $ python cfg2cnf.py [infile] [outfile] [start_symbol]

Read the description of Cfg2Cnf class for more info on the file format
"""
import codecs
from typing import TypeVar

S = TypeVar("S")


class Cfg2Cnf:
    """Convert Context-Free Grammar (CFG) to Chomsky Normal Form (CFG)

    Notes
    -----
    This class assumes the CFG to be stored in a UTF-8 file in the
    form of::

        < list of productions separated by lines >
        < format: [symbol] -> [symbol] [symbol] ... | [symbol] ... >
        < terminal symbol denoted by ' ' >

    Conversion notes:
        The CNF `S -> ε` is assumed to be valid by default

    Parameters
    ----------
    filename: str
        The CFG file path to be passed to open()
    start_sym: str
        The start symbol of the grammar

    Attributes
    ----------
    prods: dict[list[list[str]]]
        Collection of all productions, stored as dict.
        Key: production symbol, value: List of rules,
        wherein each rule contains list of symbols
    terminals: list[str]
        Collection of all terminals
    variables: list[str]
        Collection of all non-terminals
    start_sym: str
        Start symbol of the grammar

    Methods
    -------
    convert()
        Main method to convert CFG to CNF
    write(filename, complete=True)
        Write the grammar to a file
    """

    prods: dict[list[list[str]]] = {}
    start_sym: str

    def __init__(self, filename: str, start_sym: str) -> None:
        """Read CFG file and initialize attributes

        Parameters
        ----------
        filename: str
            The CFG file path to be passed to open()
        start_sym: str
            The start symbol of the grammar
        """
        with codecs.open(filename, encoding="utf-8") as f:
            for line in f:
                if "->" in line:
                    lhs, rhs = line.split("->", maxsplit=2)
                    sym = lhs.strip()
                    rules = [rule.split() for rule in rhs.split("|")]
                    if sym not in self.prods:
                        self.prods[sym] = rules
                    else:
                        self._extend_unique(self.prods[sym], rules)

        self.start_sym = start_sym

    def convert(self) -> None:
        """Convert the context-free grammar to Chomsky Normal Form.

        Reference used:
        `GeeksforGeeks <https://www.geeksforgeeks.org/converting-context-free-grammar-chomsky-normal-form/>`

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        # step 1: eliminate start symbol from RHS

        try:
            for sym in self.prods:
                for rule in self.prods[sym]:
                    if self.start_sym in rule:
                        new_sym = f"{self.start_sym}0"
                        new_prods = {new_sym: [[self.start_sym]]}
                        new_prods.update(self.prods)
                        self.prods = new_prods
                        self.start_sym = new_sym
                        raise
        except:
            pass

        # step 2a: remove null productions

        null_prods = []
        for sym in self.prods:
            if ["ε"] in self.prods[sym]:
                null_prods.append(sym)

        stack = []
        while null_prods:
            sym = null_prods.pop(0)
            self.prods[sym].remove(["ε"])

            # replace for this production first

            for rule in self.prods[sym]:
                self._extend_unique(self.prods[sym], self._replace_nullable(rule, sym))
            self._remove_all(self.prods[sym], ["ε"])
            self._remove_all(null_prods, sym)

            # replace for other productions

            for other in self.prods:
                if other != sym:
                    for rule in self.prods[other]:
                        self._extend_unique(
                            self.prods[other], self._replace_nullable(rule, sym)
                        )
                    if ["ε"] in self.prods[other]:
                        if other != self.start_sym:
                            self._append_unique(null_prods, other)
                    elif other in null_prods:
                        self._remove_all(null_prods, other)

            stack.append(sym)
            if self._is_repeating(stack):
                for sym in self.prods:
                    if sym != self.start_sym:
                        pass
                        self._remove_all(self.prods[sym], ["ε"])
                break

        # step 2b: remove unit productions

        unit_prods = []
        for sym in self.prods:
            for rule in self.prods[sym]:
                if len(rule) == 1 and not self._is_terminal(rule[0]):
                    unit_prods.append((sym, rule[0]))

        stack = []
        while unit_prods:
            sym, unit_sym = unit_prods.pop(0)
            if unit_sym in self.prods:
                if [unit_sym] in self.prods[sym]:
                    self._remove_all(self.prods[sym], [unit_sym])
                if unit_sym != sym:
                    for rule in self.prods[unit_sym]:
                        if len(rule) > 1 or self._is_terminal(rule[0]):
                            self._extend_unique(self.prods[sym], [rule])
                        elif rule[0] != unit_sym:
                            unit_prods.append([sym, rule[0]])

            stack.append((sym, unit_sym))
            if self._is_repeating(stack):
                break

        # step 2c: remove useless productions

        self.write("cfg_test.txt")
        self._remove_useless()

        # step 3: decompose terminals

        new_prods = {}
        for sym in self.prods:
            counter = 1
            new_terms = {}
            for rule in self.prods[sym]:
                terms, vrbls = self._split_rule(rule)
                if (terms and vrbls) or (len(terms) > 1):
                    for i in range(len(rule)):
                        if self._is_terminal(rule[i]):
                            if rule[i] in new_terms:
                                new_sym = new_terms[rule[i]]
                            else:
                                new_sym = f"{sym}_T{counter}"
                                new_terms[rule[i]] = new_sym
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

                if len(plus_prod) > 2:
                    plus_prods.append(plus_prod)

        self.prods.update(new_prods)

        if len(self.prods) == 1 and len(self.prods[self.start_sym]) == 0:
            self.prods[self.start_sym] = ["ε"]

    def write(self, filename: str) -> None:
        """Write the grammar (converted or not) to a file.

        Parameters
        ----------
        filename: str
            The output file path to be passed to open()
        complete: bool, optional
            Whether to write the terminals and variables alongside
            productions (default is True)

        Returns
        -------
        None
        """
        with codecs.open(filename, mode="w", encoding="utf-8") as f:
            for sym, rules in self.prods.items():
                prods_str = map(lambda p: " ".join(p), rules)
                f.write(f"{sym} -> {' | '.join(prods_str)}\n")

    def _split_rule(self, rule: list[str]) -> tuple[list[str], list[str]]:
        """
        Split a rule into list of terminals and non-terminals

        Parameters
        ----------
        rule: list[str]
            A production rule (list of symbols)

        Returns
        -------
        terms: list[str]
            List of terminal symbols (in order)
        vrbls: list[str]]
            List of non-terminal symbols (in order)
        """
        terms = []
        vrbls = []
        for sym in rule:
            if self._is_terminal(sym):
                terms.append(sym)
            else:
                vrbls.append(sym)
        return terms, vrbls

    def _replace_nullable(
        self, prod: list[list[str]], null_sym: str, __start: int = 0
    ) -> list[list[str]]:
        """Replace a nullable symbol from a production.

        It considers permutations of the nullable symbol
        in a rule using recursive approach.

        Parameters
        ----------
        prod: list[list[str]]
            The production, list of rules. Rule: list of symbols.
        null_sym: str
            The symbol which is nullable
        __start: int, optional
            Start rule position (internal recursion status)

        Returns
        -------
        result: list[list[str]]
            The production with no nullable symbol null_sym
        """
        result = []
        length = len(prod)

        for i in range(__start, length):
            if prod[i] == null_sym:
                new_rule = prod[:i] + prod[i + 1 :]

                if len(new_rule) == 0:
                    self._append_unique(result, ["ε"])
                else:
                    self._append_unique(result, new_rule)

                rec = self._replace_nullable(new_rule, null_sym, i)
                for new_rule in rec:
                    self._append_unique(result, new_rule)

        return result

    def _remove_useless(self) -> None:
        """Remove useless productions

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        # traverse from start symbol, obtain stack

        terms = []
        vrbls = [self.start_sym]
        self._traverse(self.start_sym, terms, vrbls)

        # delete items not in stack (unreachable)

        dels = []
        for sym in self.prods:
            if sym not in vrbls:
                dels.append(sym)
            for rule in self.prods[sym]:
                for rule_sym in rule:
                    if self._is_terminal(rule_sym) and rule_sym not in terms:
                        dels.append(rule_sym)

        self._delete_symbols(dels)

        # unterminable productions:
        # initialize obviously terminable productions

        terminables = []
        unterminables = []
        for sym in self.prods:
            can_terminate = False
            for rule in self.prods[sym]:
                _, vrbls = self._split_rule(rule)
                if not vrbls:
                    can_terminate = True
                    break
            if can_terminate:
                terminables.append(sym)
            else:
                unterminables.append(sym)

        # unterminable might be actually terminable, check

        stack = []
        while unterminables:
            sym = unterminables.pop(0)
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
                unterminables.append(sym)
                stack.append(sym)

            if self._is_repeating(stack):
                break

        if self.start_sym in unterminables:
            # will be true if and only if cnf is in form of S -> ε
            self._remove_all(unterminables, self.start_sym)

        self._delete_symbols(unterminables)

    def _delete_symbols(self, syms: list[str]) -> None:
        """Delete symbols from grammar (productions, variable/terminal list)

        Parameters
        ----------
        syms: list[str]
            List of symbols to be removed

        Returns
        -------
        None
        """

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

    def _traverse(self, sym: str, terms: list[str], vrbls: list[str]) -> None:
        """Traverse the grammar starting from a specified production

        It stores the terminals and non-terminals encountered

        Parameters
        ----------
        sym: str
            Start production symbol
        terms: list[str]
            Stack of terminals encountered that will be updated by the method
        vrbls: list[str]
            Stack of terminals encountered that will be updated by the method

        Returns
        -------
        None
        """
        for rule in self.prods[sym]:
            for rule_sym in rule:
                if self._is_terminal(rule_sym) and rule_sym not in terms:
                    terms.append(rule_sym)
                elif not self._is_terminal(rule_sym) and rule_sym not in vrbls:
                    vrbls.append(rule_sym)
                    self._traverse(rule_sym, terms, vrbls)

    def _is_repeating(self, visited: list[S]) -> bool:
        """Determine whether elements in a list is repeating or not.

        Useful for avoiding infinite loops and recursions

        Parameters
        ----------
        visited: list[S]
            List of "visited" elements

        Returns
        -------
        bool
        """
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

    def _is_terminal(self, sym: str) -> bool:
        return (sym[0] == "'" and sym[-1] == "'") or sym == "ε"

    def _extend_unique(self, lst: list[S], ext: list[S]) -> None:
        for val in ext:
            if val not in lst:
                lst.append(val)

    def _append_unique(self, lst: list[S], val: S) -> None:
        if val not in lst:
            lst.append(val)

    def _remove_all(self, lst: list[S], val: S) -> None:
        try:
            while True:
                lst.remove(val)
        except ValueError:
            pass


if __name__ == "__main__":
    import argparse
    import time

    parser = argparse.ArgumentParser()
    parser.add_argument("infile")
    parser.add_argument("outfile")
    parser.add_argument("start_symbol")

    args = parser.parse_args()
    t1 = time.perf_counter()

    converter = Cfg2Cnf(args.infile, args.start_symbol)
    converter.convert()
    converter.write(args.outfile)

    t2 = time.perf_counter()
    print(f"Done in {t2 - t1}s", end="\n\n")
