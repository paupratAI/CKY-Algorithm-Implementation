def read_input(file_path):
    """
    Reads a CFG in CNF format and words from a text file.

    :param file_path: Path to the input file.
    :return: A tuple containing the grammar rules and the list of words.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    grammar = {}
    words = []
    reading_grammar = True

    for line in lines:
        line = line.strip()
        if line.startswith("#"):
            continue
        if reading_grammar:
            if line == "":
                reading_grammar = False
            else:
                lhs, rhs = line.split(" -> ")
                if lhs not in grammar:
                    grammar[lhs] = []
                grammar[lhs].append(rhs.split())
        else:
            if line:
                words.append(line)
    
    return grammar, words

def cyk_algorithm(grammar, word):
    """
    Implements the CKY algorithm to determine if a word belongs to the language of a given grammar.

    :param grammar: A dictionary representing the CFG in CNF.
    :param word: A string representing the word to be checked.
    :return: True if the word belongs to the language, False otherwise.
    """
    pass



file_path = 'test_cases.txt'
grammar, words = read_input(file_path)
for word in words:
    result = cyk_algorithm(grammar, word)
    print(f"Word: {word}, Belongs to language: {result}")
