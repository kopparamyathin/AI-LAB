import random

def get_conflicts(state):
    conflicts = 0
    n = len(state)
    for i in range(n):
        for j in range(i + 1, n):
            if state[i] == state[j]:
                conflicts += 1
            elif abs(state[i] - state[j]) == abs(i - j):
                conflicts += 1
    return conflicts

def get_best_neighbor(state):
    current_conflicts = get_conflicts(state)
    best_conflicts = current_conflicts
    n = len(state)
    neighbors = []
    
    for col in range(n):
        for row in range(n):
            if state[col] == row:
                continue
            neighbor = list(state)
            neighbor[col] = row
            neighbor_conflicts = get_conflicts(neighbor)
            
            if neighbor_conflicts < best_conflicts:
                best_conflicts = neighbor_conflicts
                neighbors = [neighbor]
            elif neighbor_conflicts == best_conflicts:
                neighbors.append(neighbor)
                
    if neighbors:
        return random.choice(neighbors), best_conflicts
    return state, current_conflicts

def hill_climbing(state):
    conflicts = get_conflicts(state)
    while True:
        neighbor, neighbor_conflicts = get_best_neighbor(state)
        if neighbor_conflicts >= conflicts:
            break
        state = neighbor
        conflicts = neighbor_conflicts
    return state, conflicts

def get_user_board():
    while True:
        try:
            user_input = input().strip().split()
            if len(user_input) != 4:
                continue
            state = [int(x) for x in user_input]
            if any(x < 0 or x > 3 for x in state):
                continue
            return state
        except ValueError:
            continue

def print_chessboard(state):
    for row in range(4):
        line = ""
        for col in range(4):
            if state[col] == row:
                line += " Q "
            else:
                line += " . "
        print(line)

if __name__ == "__main__":
    initial_board = get_user_board()
    initial_h = get_conflicts(initial_board)
    
    final_board, final_h = hill_climbing(initial_board)
    
    print("Initial Board State:")
    print_chessboard(initial_board)
    print("Initial h value:", initial_h)
    print("\nFinal Board State:")
    print_chessboard(final_board)
    print("Final h value:", final_h)
