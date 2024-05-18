### Arxiu per provar que va bé la funció transform_to_FNC.
### Un cop acabat s'haurà de posar al main.py.

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
    rules = parse_grammar(grammar) # diccionari amb les regles de la gramàtica (REGLA UNITARIA)
    terminals_used = set() # set per emmagatzemar les terminals que ja s'han utilitzat (REGLA UNITARIA)

    for rule in grammar: # REGLA NO BINARIA
        lhs, rhs = rule.split(' -> ')
        rhs_parts = rhs.split(' | ')

        if len(rhs_parts) <= 2:
            continue
        else:
            pass

    for rule in grammar:
        lhs, rhs = rule.split(' -> ')
        rhs_parts = rhs.split(' | ')

        if len(rhs_parts) == 2: # REGLA HÍBRIDA
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
        else: # Just 1 rhs
            symbol = rhs_parts[0]
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
    grammar = new_rules.copy()
    return grammar


grammar = [
    'S -> A | V',
    'A -> b | C',
    'B -> D | e',
    'C -> Z',
    'Z -> z'
]

fnc_grammar = transform_to_FNC(grammar)
for rule in fnc_grammar:
    print(rule)
