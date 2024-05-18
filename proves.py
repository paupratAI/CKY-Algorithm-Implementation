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
    pass

grammar = [
    "S -> a | xA | AX | b |",
    "A -> RB",
    "B -> AX | b | a",
    "X -> a",
    "R -> XB"
]

print(parse_grammar(grammar))
'''
fnc_grammar = transform_to_FNC(grammar)
for rule in fnc_grammar:
    print(rule)
'''