from cfg import CFG

def read_input_file(file_path):
    """
    Reads a file containing grammars and words, and organizes them into a list of tuples.
    
    Args:
    file_path (str): The path to the input file.
    
    Returns:
    list of tuples: Each tuple contains a list of grammar rules and a list of words.
    """
    grammars_and_words = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        
        grammar = []
        words = []
        for line in lines:
            line = line.strip()
            if not line:
                if grammar and words:
                    grammars_and_words.append((grammar, words))
                    grammar = []
                    words = []
            elif '->' in line:
                grammar.append(line)
            else:
                words.append(line)
        
        if grammar and words:
            grammars_and_words.append((grammar, words))
    
    return grammars_and_words

def write_output_file(output_path, results):
    """
    Writes the results of the CKY algorithm to an output file.
    
    Args:
    output_path (str): The path to the output file.
    results (list of tuples): Each tuple contains a list of grammar rules 
                              and a list of results.
    """
    with open(output_path, 'w') as file:
        file.write("=" * 50 + "\n")
        for grammar, words_results in results:
            file.write("Grammar:\n")
            for rule in grammar:
                file.write(rule + "\n")
            file.write("\n")
            file.write("Results:\n")
            for word, result in words_results:
                file.write(f"{word}: {'True' if result else 'False'}\n")
            file.write("\n")
            file.write("=" * 50 + "\n")

def main():
    """
    Main function to read input, check if grammars are in CNF, execute the CKY algorithm, and write the output.
    """
    input_file_path = 'input.txt'
    output_file_path = 'output.txt'
    grammars_and_words = read_input_file(input_file_path)
    results = []

    for grammar, words in grammars_and_words:
        cfg = CFG(grammar)
        if not cfg.is_cnf:
            grammar = cfg.cnf_grammar
        
        words_results = []
        for word in words:
            result = cfg.cky_algorithm(word)
            words_results.append((word, result))
        
        results.append((grammar, words_results))
    
    write_output_file(output_file_path, results)
    print("Output written to 'output.txt'")

if __name__ == "__main__":
    main()
