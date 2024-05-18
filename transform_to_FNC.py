### EXTENSION 1 - Transform the grammar to Chomsky Normal Form (CNF)
from main import parse_grammar

def transform_to_FNC(grammar):
    """
    Transforms a grammar into Chomsky Normal Form.
    
    Args:
    grammar (list of str): A list of grammar rules.
    
    Returns:
    list of str: The grammar in Chomsky Normal Form.
    """
    def split_rule(rule): # Splits a rule into its left-hand side and right-hand side parts.
        lhs, rhs = rule.split(' -> ')
        rhs_parts = rhs.split(' | ')
        return lhs, rhs_parts

    def non_binary_rules_completed(grammar): # Checks if all rules in the grammar are binary.
        for rule in grammar:
            lhs, rhs_parts = split_rule(rule)
            if len(rhs_parts) > 2:
                return False
        return True
    
    def non_binary_rules(grammar, non_terminal_id = 0): # Transforms non-binary rules into binary rules.
        new_grammar = []
        
        for rule in grammar:
            lhs, rhs_parts = split_rule(rule)

            if len(rhs_parts) <= 2:
                new_grammar.append(rule)
            else:
                symbol1= rhs_parts[0]
                new_grammar.append(f'{lhs} -> {symbol1} | Y{non_terminal_id}')
                new_grammar.append(f'Y{non_terminal_id} -> {" | ".join(rhs_parts[1:])}')
                non_terminal_id += 1
        return new_grammar, non_terminal_id

    def hybrid_and_unitary_rules(grammar): # Transforms hybrid and unitary rules into CNF.
        new_rules = []
        non_terminal_id = 0
        terminal_to_nonterminal = {}
        rules = parse_grammar(grammar)
        terminals_used = set()

        for rule in grammar:
            lhs, rhs_parts = split_rule(rule)

            # Hybrid rule
            if len(rhs_parts) == 2: 
                new_rhs_parts = []
                for symbol in rhs_parts:
                    new_part = []
                    if symbol.islower():  # It's a terminal
                        if symbol not in terminal_to_nonterminal:
                            new_nonterminal = f'X{non_terminal_id}'
                            terminal_to_nonterminal[symbol] = new_nonterminal
                            new_rules.append(f'{new_nonterminal} -> {symbol}')
                            non_terminal_id += 1
                        new_part.append(terminal_to_nonterminal[symbol])
                    else:  # It's a non-terminal
                        new_part.append(symbol)
                    new_rhs_parts.append(''.join(new_part))
                new_rules.append(f'{lhs} -> {" | ".join(new_rhs_parts)}')
            
            # Unitary rule
            elif len(rhs_parts) == 1: # Just 1 rhs
                symbols = rhs_parts[0]      
                for symbol in symbols:
                    if symbol.islower(): # terminal
                        if symbol not in terminals_used:
                            new_rules.append(f'{lhs} -> {symbol}')
                    else: # non terminal
                        if len(rules[symbol]) == 1: # REGLA UNITARIA
                            terminal_symbol = rules[symbol][0]
                            new_rules.append(f'{lhs} -> {terminal_symbol}')
                            terminals_used.add(terminal_symbol)
                        else:
                            new_rules.append(f'{lhs} -> {symbol}')
                            new_rules.append(f'{symbol} -> {rules[symbol]}')
        return new_rules

    new_grammar = grammar.copy()

    # Transform non-binary rules into binary rules
    id = 0
    while not non_binary_rules_completed(new_grammar):
        new_grammar, id = non_binary_rules(new_grammar, id)

    # Transform hybrid and unitary rules into Chomsky Normal Form
    new_grammar = hybrid_and_unitary_rules(new_grammar)
    return new_grammar

grammar = [
    'S -> A | V | W',
    'A -> b | C',
    'B -> D | e',
    'C -> Z',
    'Z -> z',
    'M -> N | O | P',
    'Q -> R | S | T | U',
]

fnc_grammar = transform_to_FNC(grammar)
for rule in fnc_grammar:
    print(rule)
