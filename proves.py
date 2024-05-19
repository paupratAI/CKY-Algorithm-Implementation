
def transform_to_CNF(self):
    """
    Transforms a grammar into Chomsky Normal Form.
    
    Returns:
    list of str: The grammar in Chomsky Normal Form.
    """
    def split_rule(rule):
        lhs, rhs = rule.split(' -> ')
        rhs_parts = rhs.split(' | ')
        return lhs, rhs_parts
    
    def non_binary_rules_completed(grammar):
        for rule in grammar:
            lhs, rhs_parts = split_rule(rule)
            if len(rhs_parts) > 2:
                return False
        return True
    
    def get_unique_nonterminal(existing_nonterminals):
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            if letter not in existing_nonterminals:
                existing_nonterminals.add(letter)
                return letter, existing_nonterminals
        raise ValueError("Ran out of unique non-terminal symbols")
    
    def non_binary_rules(grammar, existing_nonterminals):
        new_grammar = []
        
        for rule in grammar:
            lhs, rhs_parts = split_rule(rule)
            existing_nonterminals.add(lhs)

        for rule in grammar:
            lhs, rhs_parts = split_rule(rule)

            if len(rhs_parts) <= 2:
                new_grammar.append(rule)
            else:
                symbol1= rhs_parts[0]
                symbol2, existing_nonterminals = get_unique_nonterminal(existing_nonterminals)
                new_grammar.append(f'{lhs} -> {symbol1} | {symbol2}')
                new_grammar.append(f'{symbol2} -> {" | ".join(rhs_parts[1:])}')
        return new_grammar, existing_nonterminals
    
    def hybrid_and_unitary_rules(grammar, existing_nonterminals):
        new_rules = []
        non_terminal_id = 0
        terminal_to_nonterminal = {}
        rules = self.rules
        terminals_used = set()

        for rule in grammar:
            lhs, rhs_parts = split_rule(rule)
            existing_nonterminals.add(lhs)

        for rule in grammar:
            lhs, rhs_parts = split_rule(rule)
            
            if len(rhs_parts) == 2:
                new_rhs_parts = []
                for symbol in rhs_parts:
                    new_part = []
                    if symbol.islower():
                        if symbol not in terminal_to_nonterminal:
                            new_nonterminal, existing_nonterminals  = get_unique_nonterminal(existing_nonterminals)
                            terminal_to_nonterminal[symbol] = new_nonterminal
                            new_rules.append(f'{new_nonterminal} -> {symbol}')
                            non_terminal_id += 1
                        new_part.append(terminal_to_nonterminal[symbol])
                    else:
                        new_part.append(symbol)
                    new_rhs_parts.append(''.join(new_part))
                new_rules.append(f'{lhs} -> {" | ".join(new_rhs_parts)}')
            
            elif len(rhs_parts) == 1:
                symbol = rhs_parts[0]   
                if len(symbol) == 1:
                    if symbol.islower():
                        if symbol not in terminals_used:
                            new_rules.append(f'{lhs} -> {symbol}')
                    else:
                        if len(rules[symbol]) == 1:
                            terminal_symbol = rules[symbol][0]
                            new_rules.append(f'{lhs} -> {terminal_symbol}')
                            terminals_used.add(terminal_symbol)
                        else:
                            new_rules.append(f'{lhs} -> {symbol}')
                            new_rules.append(f'{symbol} -> {rules[symbol]}')
                else:
                    new_rules.append(f'{lhs} -> {symbol}')
        return new_rules

    new_grammar = self.grammar.copy()

    existing_nonterminals = set()
    while not non_binary_rules_completed(new_grammar):
        new_grammar, existing_nonterminals = non_binary_rules(new_grammar, existing_nonterminals)

    new_grammar = hybrid_and_unitary_rules(new_grammar, existing_nonterminals)
    return new_grammar
    