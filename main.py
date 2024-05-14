def read_input(file_path):
    """
    Llegeix múltiples CFGs en CNF format i les seves paraules corresponents des d'un arxiu de text.

    :param file_path: Ruta a l'arxiu d'entrada.
    :return: Una llista de tuples, cadascuna contenint un diccionari de gramàtica i una llista de paraules.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    grammars = []
    current_grammar = {}
    current_words = []
    reading_grammar = True

    for line in lines:
        line = line.strip()
        if line.startswith("#") or not line:
            continue
        if line[0].isdigit() and line[1] == '.':
            # Inici d'una nova secció de gramàtica
            if current_grammar:
                grammars.append((current_grammar, current_words))
                current_grammar = {}
                current_words = []
            reading_grammar = True
        elif reading_grammar:
            if '->' in line:
                lhs, rhs = line.split(" -> ")  # lhs: costat esquerre, rhs: costat dret
                productions = rhs.split(" | ")
                if lhs not in current_grammar:
                    current_grammar[lhs] = []
                for production in productions:
                    current_grammar[lhs].append(production.split())
            else:
                reading_grammar = False
                current_words.append(line)
        else:
            current_words.append(line)

    if current_grammar:
        grammars.append((current_grammar, current_words))
    
    return grammars

def cyk_algorithm(grammar, word):
    """
    Implementa l'algoritme CYK per determinar si una paraula pertany al llenguatge d'una gramàtica donada.
    
    :param grammar: Un diccionari que representa la CFG en CNF.
    :param word: Una cadena que representa la paraula a verificar.
    :return: True si la paraula pertany al llenguatge, False altrament.
    """
    n = len(word)
    if n == 0:
        return False

    # Inicialitza la taula
    table = [[set() for _ in range(n)] for _ in range(n)]

    pass

# Programa principal
file_path = 'test_cases.txt'
grammars = read_input(file_path)

for i, (grammar, words) in enumerate(grammars):
    print(f"Provem gramàtica G{i+1}")
    for word in words:
        result = cyk_algorithm(grammar, word)
        print(f"Paraula: {word}, pertany al llenguatge: {result}")
    print()
