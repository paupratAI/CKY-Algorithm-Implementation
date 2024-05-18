### EXTENSION 1 - Transform the grammar to Chomsky Normal Form (CNF)
from main import parse_grammar

def find_nullable_variables(rules):
    """
    Find all nullable variables in the grammar.
    
    Args:
    rules (dict): A dictionary where keys are the left-hand side (LHS) of the rules
                  and values are lists of right-hand side (RHS) alternatives.
    
    Returns:
    set: A set of nullable variables.
    """
    nullable = set()
    # Repeat until no new nullable variables are found
    while True:
        new_nullable = set()
        for lhs, rhss in rules.items():
            for rhs in rhss:
                if all(symbol in nullable for symbol in rhs.split()):
                    new_nullable.add(lhs)
        if new_nullable.issubset(nullable):
            break
        nullable.update(new_nullable)
    return nullable

def eliminate_epsilon_productions(rules, nullable):
    """
    Eliminate ε-productions from the grammar.
    
    Args:
    rules (dict): A dictionary where keys are the left-hand side (LHS) of the rules
                  and values are lists of right-hand side (RHS) alternatives.
    nullable (set): A set of nullable variables.
    
    Returns:
    dict: Updated grammar without ε-productions.
    """
    new_rules = {}
    for lhs, rhss in rules.items():
        new_rhss = set()
        for rhs in rhss:
            symbols = rhs.split()
            n = len(symbols)
            for i in range(1 << n):
                new_rhs = [symbols[j] for j in range(n) if i & (1 << j)]
                if new_rhs or lhs not in nullable:
                    new_rhss.add(" ".join(new_rhs))
        new_rules[lhs] = list(new_rhss)
    # Remove empty RHS productions
    for lhs, rhss in new_rules.items():
        new_rules[lhs] = [rhs for rhs in rhss if rhs]
    return new_rules

def transform_to_CNF(grammar):
    """
    Transform the given CFG to CNF - step 1: Eliminate ε-Productions.
    
    Args:
    grammar (list of str): The list of grammar rules in the form "LHS -> RHS".
    
    Returns:
    dict: Updated grammar without ε-productions.
    """
    rules = parse_grammar(grammar)
    
    # Step 1: Eliminate ε-Productions
    nullable = find_nullable_variables(rules)
    rules = eliminate_epsilon_productions(rules, nullable)
    
    return rules

grammar = [
    "S -> aXbX",
    "X -> aY | bY | ",
    "Y -> X | c"
]


grammar2 = [
    "S -> a | xA | AX | b |",
    "A -> RB",
    "B -> AX | b | a",
    "X -> a",
    "R -> XB"
]

print(parse_grammar(grammar))


cnf_grammar = transform_to_CNF(grammar)
for lhs, rhss in cnf_grammar.items():
    for rhs in rhss:
        print(f"{lhs} -> {rhs}")



'''
fnc_grammar = transform_to_CNF(grammar)
for rule in fnc_grammar:
    print(rule)
'''