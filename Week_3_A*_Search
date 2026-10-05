def solve_8_puzzle(start, goal):
    def get_f(state, g):
        h = sum(abs(i//3 - goal.index(s)//3) + abs(i%3 - goal.index(s)%3)
                for i, s in enumerate(state) if s != 0)
        return g + h

    open_set = [[get_f(start, 0), 0, start]]
    parents = {start: (None, None)}
    visited = set()

    while open_set:
        open_set.sort(key=lambda x: x)
        f, g, cur = open_set.pop(0)

        if cur == goal:
            path_moves = []
            while cur:
                parent, move = parents[cur]
                if move:
                    path_moves.append(move)
                cur = parent
            return path_moves[::-1]

        visited.add(cur)
        b_idx = cur.index(0)
        r, c = b_idx // 3, b_idx % 3

        moves_map = [(-1, 0, "Up"), (1, 0, "Down"), (0, -1, "Left"), (0, 1, "Right")]
        for dr, dc, move_name in moves_map:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 3 and 0 <= nc < 3:
                n_idx = nr * 3 + nc
                nxt = list(cur)
                nxt[b_idx], nxt[n_idx] = nxt[n_idx], nxt[b_idx]
                nxt = tuple(nxt)

                if nxt not in visited and nxt not in parents:
                    parents[nxt] = (cur, move_name)
                    open_set.append([get_f(nxt, g + 1), g + 1, nxt])
    return None

def get_state_input(prompt):
    print(prompt)
    print("Enter 9 numbers (0-8) separated by spaces row by row.")
    print("Example: 1 2 3 4 5 6 7 8 0")
    while True:
        try:
            user_input = input("State: ").strip().split()
            if len(user_input) != 9:
                print("Error: Please enter exactly 9 numbers.")
                continue
            state = tuple(int(x) for x in user_input)
            if sorted(state) != list(range(9)):
                print("Error: The numbers must be 0 to 8 with no duplicates.")
                continue
            return state
        except ValueError:
            print("Error: Please enter integers only.")

if __name__ == "__main__":
    print("--- 8-PUZZLE SOLVER ---")
    start_layout = get_state_input("--- Enter Initial State ---")
    goal_layout = get_state_input("\n--- Enter Final (Goal) State ---")
    
    print("\nCalculating path...")
    moves_sequence = solve_8_puzzle(start_layout, goal_layout)
   
    if moves_sequence:
        print(f"\nSolved in {len(moves_sequence)} steps!")
        print("Sequence of moves:", " > ".join(moves_sequence))
    else:
        print("\nNo solution found (unsolvable state configuration).")
