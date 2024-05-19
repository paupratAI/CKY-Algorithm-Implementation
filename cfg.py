from transform_into_cnf import CNF

class CFG():
    def __init__(self, grammar):
        self.grammar = grammar
        self.rules = self.parse_grammar(grammar)
        self.is_cnf = self.check_if_cnf()
        self.cnf_grammar = None
        if not self.is_cnf:
            self.cnf_grammar = CNF(self.grammar).get_cnf_grammar()
        else:
            self.cnf_grammar = self.rules
    
    def parse_grammar(self, grammar):
        """
        Parses the grammar rules from a list of strings.
        
        Args:
        grammar (list of str): The list of grammar rules in the form "LHS -> RHS".
        
        Returns:
        dict: A dictionary where keys are the left-hand side (LHS) of the rules
              and values are lists of right-hand side (RHS) alternatives.
        """
        rules = {}
        for rule in grammar:
            lhs, rhs = rule.split("->")
            lhs = lhs.strip()
            rhs = [r.strip() for r in rhs.split("|")]
            rules[lhs] = rhs
        return rules

    def check_if_cnf(self):
        """
        Checks if the given grammar is in Chomsky Normal Form (CNF).
        
        Returns:
        bool: True if the grammar is in CNF, False otherwise.
        """
        rules = self.rules
        for lhs, rhs_list in rules.items():
            for rhs in rhs_list:
                if len(rhs) == 1:
                    # Single terminal symbol (must be lowercase)
                    if not rhs.islower():  # rhs is a single terminal
                        return False
                elif len(rhs) == 2:
                    # Two symbols (both must be non-terminals)
                    if not (rhs[0].isupper() and rhs[1].isupper()):
                        return False
                else:
                    return False  # If there are more than 2 symbols on the right-hand side, it's not CNF
        return True  # If all checks passed, it's CNF

    def cky_algorithm(self, word):
        """
        Implements the Cocke-Kasami-Younger (CKY) algorithm to determine if a word 
        can be generated by a given grammar.

        Args:
        word (str): The word to be tested.

        Returns:
        bool: True if the word can be generated by the grammar, False otherwise.
        """
        rules = self.cnf_grammar  # Use the CNF grammar
        n = len(word)
        table = [[set() for _ in range(n)] for _ in range(n)]

        # Fill the diagonal of the table
        for j in range(n):
            for lhs, rhs_list in rules.items():
                for rhs in rhs_list:
                    if rhs == word[j]:
                        table[j][j].add(lhs)

            # Handle unit productions for the diagonal
            self.handle_unit_productions(j, j, table)

        # Fill the rest of the table
        for span in range(2, n + 1):
            for i in range(n - span + 1):
                j = i + span - 1
                for k in range(i, j):
                    for lhs, rhs_list in rules.items():
                        for rhs in rhs_list:
                            if len(rhs) == 2:
                                B, C = rhs
                                if B in table[i][k] and C in table[k + 1][j]:
                                    table[i][j].add(lhs)

                # Handle unit productions for the current cell
                self.handle_unit_productions(i, j, table)

        return 'S' in table[0][n-1]

    def handle_unit_productions(self, i, j, table):
        """
        Handles the addition of unit productions in the CKY table.

        Args:
        i (int): The row index in the CKY table.
        j (int): The column index in the CKY table.
        table (list of list of set): The CKY table.
        """
        rules = self.cnf_grammar  # Use the CNF grammar
        added = True
        while added:
            added = False
            for lhs, rhs_list in rules.items():
                for rhs in rhs_list:
                    if len(rhs) == 1 and rhs in table[i][j]:
                        if lhs not in table[i][j]:
                            table[i][j].add(lhs)
                            added = True
