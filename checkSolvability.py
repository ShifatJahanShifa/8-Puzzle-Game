def is_solvable(N):
    inv = 0
    for i in range(8):  # Check solvability by counting inversions
        for j in range(i + 1, 9):
            if N[i] > N[j] and N[j] != 0:
                inv += 1
    if inv % 2 != 0:  # If odd, not solvable
        print("No solution exists for this initial state")
        return False
    return True
