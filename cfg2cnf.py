# File      : cfg2cnf.py
# Author    : Hilya Fadhilah Imania
# Created   : 2021/11/21
# Version   : 0.0.1
import codecs
from typing import TypeVar

def cfgToCnf(filename: str, start_sym: str):

    # read file, put raw rules to dict

    prods = {}
    with codecs.open(filename, encoding='utf-8') as f:
        for line in f:
            lhs, rhs = line.split('->', maxsplit=2)
            sym = lhs.strip()
            rules = [rule.split() for rule in rhs.split('|')]
            prods[sym] = rules

    print_prods(prods)

    # step 1: eliminate start symbol from RHS

    try:
        for rule in prods[start_sym]:
            if start_sym in rule:
                new_sym = f"{start_sym}0"
                new_prods = { new_sym: [[start_sym]] }
                new_prods.update(prods)
                prods = new_prods
                start_sym = new_sym
                raise
    except:
        pass

    # step 2a: remove null productions

    null_prods = []
    for sym in prods:
        if ['ε'] in prods[sym]:
            print(sym)
            null_prods.append(sym)

    while null_prods:
        sym = null_prods.pop(0)
        prods[sym].remove(['ε'])

        # replace for this production first

        for rule in prods[sym]:
            extend_unique(prods[sym], replace_nullable(sym, rule))

        # replace for other productions

        for other in prods:
            if other != sym:
                for rule in prods[other]:
                    extend_unique(prods[other], replace_nullable(sym, rule))
                if ['ε'] in prods[other]:
                    null_prods.insert(0, other)

    print_prods(prods)

    # step 2b: remove unit productions

    unit_prods = []
    for sym in prods:
        for rule in prods[sym]:
            if len(rule) == 1 and not is_terminal(rule[0]):
                unit_prods.append((sym, rule[0]))

    while unit_prods:
        sym, unit_sym = unit_prods.pop()
        if unit_sym in prods:
            prods[sym].remove([unit_sym])
            if unit_sym != sym:
                for rule in prods[unit_sym]:
                    if len(rule) > 1 or is_terminal(rule[0]):
                        extend_unique(prods[sym], [rule])
                    else:
                        unit_prods.append([sym, rule[0]])

    print_prods(prods)

    # step 2c: remove useless productions

    remove_useless(prods, start_sym)
    print_prods(prods)

    # step 3: decompose terminals

    new_prods = {}
    for sym in prods:
        counter = 1
        new_terms = {}
        for rule in prods[sym]:
            terms, syms = split_rule(rule)
            if (terms and syms) or (len(terms) > 1):
                for i in range(len(rule)):
                    if is_terminal(rule[i]):
                        if rule[i] in new_terms:
                            new_sym = new_terms[rule[i]]
                        else:
                            new_sym = f'{sym}_T{counter}'
                            new_terms[rule[i]] = new_sym
                            counter += 1
                        rule[i] = new_sym

        for term, new_sym in new_terms.items():
            new_prods[new_sym] = [[term]]

    # step 4: decompose symbols

        plus_prods = []
        for rule in prods[sym]:
            if len(rule) > 2:
                plus_prods.append(rule)

        while plus_prods:
            rule = plus_prods.pop()

            plus_prod = rule[1:]
            new_sym = f'{sym}_S{counter}'
            new_prods[new_sym] = [plus_prod]
            del rule[1:]
            rule.append(new_sym)
            counter += 1

            if len(plus_prod) > 2:
                plus_prods.append(plus_prod)

    prods.update(new_prods)
    print_prods(prods)

    return prods, start_sym

def replace_nullable(null_sym: str, prod: list[str], start: int = 0) -> list[str]:
    result = []
    length = len(prod)

    for i in range(start, length):
        if prod[i] == null_sym:
            new_rule = prod[:i] + prod[i+1:]

            if len(new_rule) == 0:
                append_unique(result, ['ε'])
            else:
                append_unique(result, new_rule)

            rec = replace_nullable(null_sym, new_rule, i)
            for new_rule in rec:
                append_unique(result, new_rule)

    return result

def remove_useless(prods: dict[list[str]], start_sym: str):
    
    # traverse from start symbol, obtain stack

    stack = []
    traverse(prods, start_sym, stack)

    # delete items not in stack (unreachable)

    dels = []
    for sym in prods:
        if sym != start_sym and sym not in stack:
            dels.append(sym)

    for sym in dels:
        del prods[sym]

    # unterminable productions:
    # initialize obviously terminable productions

    terminables = []
    unterminables = []
    for sym in prods:
        can_terminate = False
        for rule in prods[sym]:
            _, syms = split_rule(rule)
            if not syms:
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
        for rule in prods[sym]:
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

        if is_repeating(stack):
            break

    # delete rules with unterminable symbol

    for sym in prods:
        rules = []
        for rule in prods[sym]:
            can_terminate = True
            for rule_sym in rule:
                if not is_terminal(rule_sym) and rule_sym in unterminables:
                    can_terminate = False
                    break
            if can_terminate:
                rules.append(rule)
        prods[sym] = rules

    # delete unterminable productions

    for sym in unterminables:
        del prods[sym]

def traverse(prods: dict[list[str]], sym: str, stack: list[str]):
    for rule in prods[sym]:
        for rule_sym in rule:
            if not is_terminal(rule_sym) and rule_sym not in stack:
                stack.append(rule_sym)
                traverse(prods, rule_sym, stack)

S = TypeVar('S')

def is_repeating(visited: list[S]) -> bool:
    unrepeated = []
    for i in range(len(visited)):
        try:
            j = -1 
            while True:
                j = unrepeated.index(visited[i], j + 1)
                if visited[i+1] == unrepeated[j+1]:
                    return True
        except:
            pass
        unrepeated.append(visited[i])
    return False

def extend_unique(lst: list[S], ext: list[S]):
    for val in ext:
        if val not in lst:
            lst.append(val)

def append_unique(lst: list[S], val: S):
    if val not in lst:
        lst.append(val)

def is_terminal(sym: str) -> bool:
    return sym[0] == "'" and sym[-1] == "'"

def split_rule(rule: list[str]) -> tuple[list[str], list[str]]:
    terms = []
    syms = []
    for sym in rule:
        if is_terminal(sym):
            terms.append(sym)
        else:
            syms.append(sym)
    return terms, syms

def print_prods(rules):
    for sym in rules:
        prods_str = map(lambda p: ' '.join(p), rules[sym])
        print(f"{sym} -> {' | '.join(prods_str)}")
    print('')

if __name__ == '__main__':
    cfgToCnf('test2.txt', 'S')