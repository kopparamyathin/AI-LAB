
from itertools import product
import re

def implication(p, q):
    return (not p) or q

def biconditional(p, q):
    return p == q

def tokenize(expression):
    pattern = r'<->|->|[A-Za-z][A-Za-z0-9_]*|[()~&|]'
    return re.findall(pattern, expression.replace(" ", ""))

class Parser:
    def __init__(self, tokens, model):
        self.tokens = tokens
        self.model = model
        self.position = 0

    def current(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

    def eat(self, token=None):
        current = self.current()

        if token is not None and current != token:
            raise ValueError(f"Expected '{token}' but found '{current}'")

        self.position += 1
        return current

    def parse_biconditional(self):
        left = self.parse_implication()

        while self.current() == "<->":
            self.eat("<->")
            right = self.parse_implication()
            left = biconditional(left, right)

        return left

    def parse_implication(self):
        left = self.parse_or()

        if self.current() == "->":
            self.eat("->")
            right = self.parse_implication()
            left = implication(left, right)

        return left

    def parse_or(self):
        left = self.parse_and()

        while self.current() == "|":
            self.eat("|")
            right = self.parse_and()
            left = left or right

        return left

    def parse_and(self):
        left = self.parse_not()

        while self.current() == "&":
            self.eat("&")
            right = self.parse_not()
            left = left and right

        return left

    def parse_not(self):
        if self.current() == "~":
            self.eat("~")
            return not self.parse_not()

        return self.parse_primary()

    def parse_primary(self):
        token = self.current()

        if token == "(":
            self.eat("(")
            value = self.parse_biconditional()
            self.eat(")")
            return value

        if token is None:
            raise ValueError("Unexpected end of expression")

        if token in self.model:
            self.eat()
            return self.model[token]

        raise ValueError(f"Unknown symbol: {token}")

def evaluate(expression, model):
    tokens = tokenize(expression)
    parser = Parser(tokens, model)
    result = parser.parse_biconditional()

    if parser.current() is not None:
        raise ValueError(f"Unexpected token: {parser.current()}")

    return result

def get_symbols(expressions):
    symbols = set()

    for expression in expressions:
        tokens = tokenize(expression)

        for token in tokens:
            if re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*', token):
                symbols.add(token)

    return sorted(symbols)

def build_kb(statements):
    return " & ".join(f"({statement})" for statement in statements)

def print_truth_table(symbols, rows, statements, queries):
    headers = symbols + [f"S{i}" for i in range(1, len(statements) + 1)] + ["KB"] + [f"Q{i}" for i in range(1, len(queries) + 1)]

    print("\nTRUTH TABLE")
    print(" | ".join(headers))
    print("-" * (len(" | ".join(headers))))

    for row in rows:
        values = []

        for symbol in symbols:
            values.append("T" if row[symbol] else "F")

        for i in range(1, len(statements) + 1):
            values.append("T" if row[f"S{i}"] else "F")

        values.append("T" if row["KB"] else "F")

        for i in range(1, len(queries) + 1):
            values.append("T" if row[f"Q{i}"] else "F")

        print(" | ".join(values))

def main():
    print("PROPOSITIONAL LOGIC - TRUTH TABLE ENUMERATION")

    print("\nOperators: ~ NOT, & AND, | OR, -> IMPLICATION, <-> BICONDITIONAL")

    statements = []

    print("\nEnter KB statements (0 to stop):")

    while True:
        statement = input(f"KB {len(statements) + 1}: ").strip()

        if statement == "0":
            break

        if statement:
            statements.append(statement)

    if not statements:
        print("Error: Knowledge Base cannot be empty.")
        return

    print("\nKnowledge Base:")
    for i, statement in enumerate(statements, 1):
        print(f"S{i}: {statement}")

    queries = []

    print("\nEnter queries (0 to stop):")

    while True:
        query = input(f"Query {len(queries) + 1}: ").strip()

        if query == "0":
            break

        if query:
            queries.append(query)

    if not queries:
        print("No queries entered.")
        return

    symbols = get_symbols(statements + queries)
    rows = []

    for values in product([False, True], repeat=len(symbols)):
        model = dict(zip(symbols, values))
        row = model.copy()

        for i, statement in enumerate(statements, 1):
            row[f"S{i}"] = evaluate(statement, model)

        row["KB"] = all(row[f"S{i}"] for i in range(1, len(statements) + 1))

        for i, query in enumerate(queries, 1):
            row[f"Q{i}"] = evaluate(query, model)

        rows.append(row)

    print_truth_table(symbols, rows, statements, queries)

    print("\nENTAILMENT RESULTS")

    for i, query in enumerate(queries, 1):
        entails = all(not row["KB"] or row[f"Q{i}"] for row in rows)

        print(f"\nQuery {i}: {query}")

        if entails:
            print("Result: YES")
            print(f"KB |= {query}")
        else:
            print("Result: NO")
            print(f"KB !|= {query}")

if __name__ == "__main__":
    main()
