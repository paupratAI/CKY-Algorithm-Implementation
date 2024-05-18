from main import parse_grammar
def transform_to_FNC(grammar):
    """
    Transforms a grammar into Chomsky Normal Form.
    
    Args:
    grammar (list of str): A list of grammar rules.
    
    Returns:
    list of str: The grammar in Chomsky Normal Form.
    """
    def split_rule(rule):
        lhs, rhs = rule.split(' -> ')
        rhs_parts = rhs.split(' | ')
        return lhs, rhs_parts

    def non_binary_rules(grammar):
        new_grammar = []
        non_terminal_id = 0
        
        for rule in grammar:
            lhs, rhs_parts = split_rule(rule)

            if len(rhs_parts) <= 2:
                new_grammar.append(rule)
            else:
                symbol1, symbol2, symbol3 = rhs_parts[0], rhs_parts[1], rhs_parts[2]
                new_grammar.append(f'{lhs} -> {symbol1} | Y{non_terminal_id}')
                new_grammar.append(f'Y{non_terminal_id} -> {symbol2} | {symbol3}')
                non_terminal_id += 1
                '''while len(rhs_parts) > 2:
                    new_non_terminal = f'Y{non_terminal_id}'
                    new_grammar.append(f'{lhs} -> {rhs_parts[0]} | {new_non_terminal}')
                    lhs = new_non_terminal
                    rhs_parts = rhs_parts[1:]
                    non_terminal_id += 1
                new_grammar.append(f'{lhs} -> {" | ".join(rhs_parts)}')'''

        return new_grammar

    def hybrid_and_unitary_rules(grammar):
        new_rules = []
        non_terminal_id = 0
        terminal_to_nonterminal = {}
        rules = parse_grammar(grammar)
        terminals_used = set()

        for rule in grammar:
            lhs, rhs_parts = split_rule(rule)

            if len(rhs_parts) == 2: # REGLA HIBRIDA
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

        return new_rules


    new_grammar = non_binary_rules(grammar)
    grammar_fnc = hybrid_and_unitary_rules(new_grammar)
    return grammar_fnc

grammar = [
    'S -> A | V',
    'A -> b | C',
    'B -> D | e',
    'C -> Z',
    'Z -> z',
    'M -> N | O | P',
    'Q -> R | S | T ',
]

fnc_grammar = transform_to_FNC(grammar)
for rule in fnc_grammar:
    print(rule)
