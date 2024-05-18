### Arxiu per provar que va bé la funció transform_to_FNC.
### Un cop acabatt s'haurà de posar al main.py.

from main import parse_grammar

def transform_to_FNC(grammar):
    """
    Transforms a grammar into Chomsky Normal Form.
    
    Args:
    grammar (list of str): A list of grammar rules.
    
    Returns:
    list of str: The grammar in Chomsky Normal Form.
    """
    new_rules = []
    terminal_to_nonterminal = {}
    next_nonterminal_id = 0

    for rule in grammar:
        lhs, rhs = rule.split(' -> ')
        rhs_parts = rhs.split(' | ')
        new_rhs_parts = []

        for symbol in rhs_parts:
            new_part = []
            if symbol.islower():  # It's a terminal
                if symbol not in terminal_to_nonterminal:
                    new_nonterminal = f'X{next_nonterminal_id}'
                    terminal_to_nonterminal[symbol] = new_nonterminal
                    new_rules.append(f'{new_nonterminal} -> {symbol}')
                    next_nonterminal_id += 1
                new_part.append(terminal_to_nonterminal[symbol])
            else:  # It's a non-terminal
                new_part.append(symbol)
            new_rhs_parts.append(''.join(new_part))

        new_rules.append(f'{lhs} -> {" | ".join(new_rhs_parts)}')

    return new_rules


grammar = [
    'S -> A | V',
    'A -> b | C',
    'B -> D | e',
    'C -> x | y',
]

fnc_grammar = transform_to_FNC(grammar)
for rule in fnc_grammar:
    print(rule)
