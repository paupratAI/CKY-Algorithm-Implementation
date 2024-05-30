### Extension 1 - Convert CFG to CNF to Chomsky Normal Form (CNF) ###

class CNF():
    def __init__(self, rules):
        self.rules = rules
        self.existing_nonterminals = set(self.rules.keys())
        self.cnf_grammar = self.transform_to_CNF()

    def get_unique_nonterminal(self):
        """
        Generates a unique non-terminal symbol that does not exist in the current set.
        
        Returns:
        str: A unique non-terminal symbol.
        """
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            if letter not in self.existing_nonterminals:
                self.existing_nonterminals.add(letter)
                return letter
        raise ValueError("Ran out of unique non-terminal symbols")

    def remove_null_productions(self):
        """
        Removes null productions from the grammar.
        
        Returns:
        dict: The updated grammar rules without null productions.
        """
        rules = self.rules
        nullable = set()

        # Step 1: Find nullable variables
        for lhs, rhs_list in rules.items():
            for rhs in rhs_list:
                if rhs == "":
                    nullable.add(lhs)

        changed = True
        while changed:
            changed = False
            for lhs, rhs_list in rules.items():
                for rhs in rhs_list:
                    if all(symbol in nullable for symbol in rhs):
                        if lhs not in nullable:
                            nullable.add(lhs)
                            changed = True

        # Step 2: Remove null productions and add new rules
        new_rules = {}
        for lhs, rhs_list in rules.items():
            new_rhs_list = set()
            for rhs in rhs_list:
                if rhs != "":
                    # Add the production without changes
                    new_rhs_list.add(rhs)
                    # Add productions omitting nullable variables
                    subsets = self.get_nullable_subsets(rhs, nullable)
                    subsets.discard("")  # Remove the empty string from subsets
                    new_rhs_list.update(subsets)
            if new_rhs_list:
                new_rules[lhs] = list(new_rhs_list)
        self.rules = new_rules

    def get_nullable_subsets(self, rhs, nullable):
        """
        Generates all possible subsets of RHS by omitting nullable variables.
        
        Args:
        rhs (str): The right-hand side of a production.
        nullable (set): The set of nullable variables.
        
        Returns:
        set: A set of new RHS strings with nullable variables omitted.
        """
        if not rhs:
            return {""}
        first, rest = rhs[0], rhs[1:]
        subsets = self.get_nullable_subsets(rest, nullable)
        if first in nullable:
            return subsets | {first + subset for subset in subsets}
        else:
            return {first + subset for subset in subsets}

    def unitary_rule(self):
        """
        Removes unit productions from the grammar.
        
        Returns:
        dict: The updated grammar rules without unit productions.
        """
        rules = self.rules
        unit_productions = [(lhs, rhs[0]) for lhs, rhs_list in rules.items() for rhs in rhs_list if len(rhs) == 1 and rhs.isupper()]
        
        while unit_productions:
            lhs, unit = unit_productions.pop()
            if lhs not in rules:
                continue
            if lhs != unit:
                if lhs not in rules:
                    rules[lhs] = []
                if unit in rules:  # Ensure the unit production exists in rules
                    for rhs in rules[unit]:
                        if rhs not in rules[lhs]:
                            rules[lhs].append(rhs)
                            if len(rhs) == 1 and rhs.isupper():
                                unit_productions.append((lhs, rhs))
                rules[lhs] = [r for r in rules[lhs] if r != unit]

        self.rules = {lhs: rhs for lhs, rhs in rules.items() if rhs}

    def hybrid_rule(self):
        """
        Eliminates terminals from the RHS of productions if they exist with other non-terminals or terminals.
        
        Returns:
        dict: The updated grammar rules with terminals eliminated from RHS.
        """
        rules = self.rules
        new_rules = {}
        terminal_to_var = {}

        for lhs, rhs_list in rules.items():
            new_rhs_list = []
            for rhs in rhs_list:
                if len(rhs) > 1:
                    new_rhs = []
                    for symbol in rhs:
                        if symbol.islower():  # If it's a terminal
                            if symbol not in terminal_to_var:
                                new_var = self.get_unique_nonterminal()
                                terminal_to_var[symbol] = new_var
                                if new_var not in new_rules:
                                    new_rules[new_var] = [symbol]
                            new_rhs.append(terminal_to_var[symbol])
                        else:
                            new_rhs.append(symbol)
                    new_rhs_list.append("".join(new_rhs))
                else:
                    new_rhs_list.append(rhs)
            if lhs not in new_rules:
                new_rules[lhs] = []
            new_rules[lhs].extend(new_rhs_list)

        self.rules = new_rules


    def non_binary_rule(self):
        """
        Eliminates productions with more than two non-terminals on the RHS.
        
        Returns:
        dict: The updated grammar rules with RHS having at most two non-terminals.
        """
        rules = self.rules
        new_rules = {}

        for lhs, rhs_list in rules.items():
            new_rhs_list = []
            for rhs in rhs_list:
                while len(rhs) > 2:
                    new_var = self.get_unique_nonterminal()
                    new_rules[new_var] = [rhs[-2:]]
                    rhs = rhs[:-2] + new_var
                new_rhs_list.append(rhs)
            if lhs not in new_rules:
                new_rules[lhs] = []
            new_rules[lhs].extend(new_rhs_list)

        self.rules = new_rules

    def is_binary(self):
        """
        Checks if all productions have at most two non-terminal symbols in the RHS.
        
        Returns:
        bool: True if all productions have at most two non-terminal symbols in the RHS, False otherwise.
        """
        for rhs_list in self.rules.values():
            for rhs in rhs_list:
                non_terminals = [symbol for symbol in rhs if symbol.isupper()]
                if len(non_terminals) > 2:
                    return False
        return True

    def transform_to_CNF(self):
        """
        Transforms the grammar to Chomsky Normal Form (CNF).
        
        Returns:
        dict: The CNF grammar rules.
        """
        self.remove_null_productions()
        self.unitary_rule()
        self.hybrid_rule()
        while not self.is_binary():
            self.non_binary_rule()

        # Ensure 'S' is the first key in the rules dictionary
        if 'S' in self.rules:
            ordered_rules = {'S': self.rules['S']}
            for key in self.rules:
                if key != 'S':
                    ordered_rules[key] = self.rules[key]
            self.rules = ordered_rules
        
        return self.rules

    def get_cnf_grammar(self):
        return self.cnf_grammar
