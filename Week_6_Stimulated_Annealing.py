
import random
import math

def calculate_cost(board):
    conflicts = 0
    for c1 in range(8):
        for c2 in range(c1 + 1, 8):
            r1 = board[c1]
            r2 = board[c2]

            if r1 == r2 or abs(r1 - r2) == abs(c1 - c2):
                conflicts += 1

    return conflicts

def get_neighbor(board):
    next_board = board.copy()
    col = random.randint(0, 7)
    new_row = random.randint(0, 7)

    while new_row == next_board[col]:
        new_row = random.randint(0, 7)

    next_board[col] = new_row
    return next_board

def print_board(board):
    for row in range(8):
        for col in range(8):
            if board[col] == row:
                print("Q", end=" ")
            else:
                print(".", end=" ")
        print()

def simulated_annealing():
    current = [0, 1, 2, 3, 4, 5, 6, 7]
    T = 10.0
    alpha = 0.90

    print("Initial State:", current)
    print("Initial Cost:", calculate_cost(current))

    while T > 0.001:
        if calculate_cost(current) == 0:
            break

        next_state = get_neighbor(current)

        delta_E = calculate_cost(current) - calculate_cost(next_state)

        if delta_E > 0:
            current = next_state
        else:
            probability = math.exp(delta_E / T)

            if random.random() < probability:
                current = next_state

        T = T * alpha

    print("\nFINAL RESULT")
    print("Final State:", current)
    print("Final Cost:", calculate_cost(current))

    print("\nChess Board:")
    print_board(current)

    if calculate_cost(current) == 0:
        print("Solution Found!")
    else:
        print("Solution Not Found.")

    return current

simulated_annealing()

