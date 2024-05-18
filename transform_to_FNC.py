### EXTENSIÓ 1 - Transformar la gramàtica a la forma normal de Chomsky (FNC)
from main import parse_grammar

def transform_to_FNC(grammar):
    """
    Transforms a grammar into Chomsky Normal Form.
    
    Args:
    grammar (list of str): A list of grammar rules.
    
    Returns:
    list of str: The grammar in Chomsky Normal Form.
    """
    new_grammar = []
    non_terminal_id_rule3 = 0 # index per anar creant Y0, Y1, Y2... (REGLA NO BINARIA)
    for rule in grammar: # REGLA NO BINARIA
        lhs, rhs = rule.split(' -> ')
        rhs_parts = rhs.split(' | ')

        if len(rhs_parts) <= 2:
            new_grammar.append(rule)
            continue
        else:
            symbol1, symbol2, symbol3 = rhs_parts[0], rhs_parts[1], rhs_parts[2]
            new_grammar.append(f'{lhs} -> {symbol1} | Y{non_terminal_id_rule3}')
            new_grammar.append(f'Y{non_terminal_id_rule3} -> {symbol2} | {symbol3}')
            non_terminal_id_rule3 += 1

    new_rules = []
    non_terminal_id_rule1 = 0 # index per anar creant X0, X1, X2... (REGLA HIBRIDA)
    terminal_to_nonterminal_rule1 = {} # diccionari per anar emmagatzemant X0, X1, X2... (REGLA HIBRIDA)
    rules = parse_grammar(new_grammar) # diccionari amb les regles de la gramàtica (REGLA UNITARIA)
    terminals_used = set() # set per emmagatzemar les terminals que ja s'han utilitzat (REGLA UNITARIA)

    for rule in new_grammar:
        lhs, rhs = rule.split(' -> ')
        rhs_parts = rhs.split(' | ')

        if len(rhs_parts) == 2: # REGLA HIBRIDA
            new_rhs_parts = []
            for symbol in rhs_parts:
                new_part = []
                if symbol.islower():  # It's a terminal
                    if symbol not in terminal_to_nonterminal_rule1:
                        new_nonterminal = f'X{non_terminal_id_rule1}'
                        terminal_to_nonterminal_rule1[symbol] = new_nonterminal
                        new_rules.append(f'{new_nonterminal} -> {symbol}')
                        non_terminal_id_rule1 += 1
                    new_part.append(terminal_to_nonterminal_rule1[symbol])
                else:  # It's a non-terminal
                    new_part.append(symbol)
                new_rhs_parts.append(''.join(new_part))
            new_rules.append(f'{lhs} -> {" | ".join(new_rhs_parts)}')
        elif len(rhs_parts) == 1: # Just 1 rhs
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
    grammar_fnc = new_rules.copy()
    return grammar_fnc


grammar = [
    'S -> A | V',
    'A -> b | C',
    'B -> D | e',
    'C -> Z',
    'Z -> z',
    'M -> N | O | P'
]

fnc_grammar = transform_to_FNC(grammar)
for rule in fnc_grammar:
    print(rule)
