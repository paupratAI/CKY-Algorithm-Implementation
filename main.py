def parse_grammar(grammar):
    rules = {}
    for rule in grammar:
        lhs, rhs = rule.split("->")
        lhs = lhs.strip()
        rhs = [r.strip() for r in rhs.split("|")]
        rules[lhs] = rhs
    return rules

def cky_algorithm(grammar, word):
    rules = parse_grammar(grammar)
    n = len(word)
    table = [[set() for _ in range(n)] for _ in range(n)]
    
    for j in range(1, n + 1):
        for lhs, rhs_list in rules.items():
            for rhs in rhs_list:
                if rhs == word[j-1]:
                    table[j-1][j-1].add(lhs)
        for i in range(j-2, -1, -1):
            for k in range(i+1, j):
                for lhs, rhs_list in rules.items():
                    for rhs in rhs_list:
                        if len(rhs) == 2 and rhs[0] in table[i][k-1] and rhs[1] in table[k][j-1]:
                            table[i][j-1].add(lhs)
    
    return 'S' in table[0][n-1]

# Ejemplo de uso
grammar = [
    "S -> a | XA | AX | b",
    "A -> RB",
    "B -> AX | b | a",
    "X -> a",
    "R -> XB",
]
words = ["a", "b", "aa", "ab", "ba", "abaa"]
for word in words:
    print(cky_algorithm(grammar, word)) 

print()
grammar2 = [
    "S -> AB | CD | CB | SS",
    "A -> BC | a",
    "B -> SC | b",
    "C -> DD | b",
    "D -> BA"
]

words2 = ["ab", "ba", "aabb", "abab", "baba"]

for word in words2:
    print(cky_algorithm(grammar2, word))