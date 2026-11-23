import copy
import itertools
import re


def parse_expression(text):
  text = text.replace(" ", "")
  if not text:
    return ""
  if "(" not in text:
    return text

  match = re.match(r"^([A-Za-z0-9_]+)\((.*)\)$", text)
  if not match:
    raise ValueError("Invalid expression: " + text)

  name, args_string = match.group(1), match.group(2)
  args, current, depth = [], "", 0

  for char in args_string:
    if char == "," and depth == 0:
      args.append(current)
      current = ""
    else:
      current += char
      if char == "(":
        depth += 1
      elif char == ")":
        depth -= 1
  if current:
    args.append(current)

  return [name] + [parse_expression(arg) for arg in args]


def format_expression(expr):
  if isinstance(expr, str):
    return expr
  if isinstance(expr, list):
    if len(expr) == 1:
      return expr[0]
    return (
        expr[0]
        + "("
        + ", ".join(format_expression(arg) for arg in expr[1:])
        + ")"
    )
  return str(expr)


def is_variable(term):
  if not isinstance(term, str):
    return False
  return term.islower() and (len(term) == 1 or "_" in term)


def occurs(variable, expression):
  if variable == expression:
    return True
  if isinstance(expression, list):
    return any(occurs(variable, arg) for arg in expression[1:])
  return False


def apply_substitution(substitution, expression):
  if isinstance(expression, str):
    visited = set()
    while expression in substitution:
      if expression in visited:
        break
      visited.add(expression)
      expression = substitution[expression]
    return expression
  if isinstance(expression, list):
    return [expression[0]] + [
        apply_substitution(substitution, arg) for arg in expression[1:]
    ]
  return expression


def unify(x, y, substitution=None):
  if substitution is None:
    substitution = {}
  else:
    substitution = substitution.copy()

  x = apply_substitution(substitution, x)
  y = apply_substitution(substitution, y)

  if x == y:
    return substitution
  if is_variable(x):
    if occurs(x, y):
      return None
    substitution[x] = y
    return substitution
  if is_variable(y):
    if occurs(y, x):
      return None
    substitution[y] = x
    return substitution
  if isinstance(x, list) and isinstance(y, list):
    if x[0] != y[0] or len(x) != len(y):
      return None
    for i in range(1, len(x)):
      substitution = unify(x[i], y[i], substitution)
      if substitution is None:
        return None
    return substitution
  return None


def standardize_variables(rule, counter):
  premises, conclusion = rule
  mapping = {}

  def rename(expr):
    if is_variable(expr):
      if expr not in mapping:
        mapping[expr] = f"{expr}_{counter}"
      return mapping[expr]
    if isinstance(expr, list):
      return [expr[0]] + [rename(arg) for arg in expr[1:]]
    return expr

  return ([rename(p) for p in premises], rename(conclusion))


def fol_fc_ask(kb_facts, kb_rules, query):
  facts = [copy.deepcopy(f) for f in kb_facts]
  rule_counter = 0

  for fact in facts:
    if unify(fact, query) is not None:
      return True

  while True:
    new_facts = []

    for rule in kb_rules:
      rule_counter += 1
      premises, conclusion = standardize_variables(rule, rule_counter)

      for fact_combo in itertools.product(facts, repeat=len(premises)):
        theta = {}
        matched = True

        for premise, fact in zip(premises, fact_combo):
          theta = unify(premise, fact, theta)
          if theta is None:
            matched = False
            break

        if matched:
          inferred = apply_substitution(theta, conclusion)

          if inferred not in facts and inferred not in new_facts:
            new_facts.append(inferred)
            print("Inferred:", format_expression(inferred))

            if unify(inferred, query) is not None:
              return True

    if not new_facts:
      return False

    facts.extend(new_facts)


def parse_rule(rule_str):
  if "->" not in rule_str:
    raise ValueError("Rule must contain '->'")

  lhs, rhs = rule_str.split("->")
  premises = []
  current = ""
  depth = 0

  for char in lhs:
    if char == "," and depth == 0:
      if current.strip():
        premises.append(parse_expression(current.strip()))
      current = ""
    else:
      current += char
      if char == "(":
        depth += 1
      elif char == ")":
        depth -= 1

  if current.strip():
    premises.append(parse_expression(current.strip()))

  conclusion = parse_expression(rhs.strip())
  return (premises, conclusion)


def main():
  print("FIRST-ORDER LOGIC FORWARD CHAINING\n")

  try:
    n_facts = int(input("Enter number of facts: "))
    facts = []
    for i in range(n_facts):
      fact_str = input(f"Fact {i + 1}: ")
      facts.append(parse_expression(fact_str))

    n_rules = int(input("\nEnter number of rules (Format: P1(x), P2(x) -> Q(x)): "))
    rules = []
    for i in range(n_rules):
      rule_str = input(f"Rule {i + 1}: ")
      rules.append(parse_rule(rule_str))

    query_str = input("\nEnter query: ")
    query = parse_expression(query_str)

    print("\n--- INFERENCE TRACE ---")
    result = fol_fc_ask(facts, rules, query)

    print("\nResult:", "PROVEN (True)" if result else "CANNOT PROVE (False)")

  except Exception as e:
    print("Error:", e)


if __name__ == "__main__":
  main()
