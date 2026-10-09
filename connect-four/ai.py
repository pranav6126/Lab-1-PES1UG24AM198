import random


class AI:
    def choose_column(self, board, me="O", opponent="X"):
        # Starter AI is deliberately basic; students improve it in Task 3.
        legal = [c for c in range(7) if board.grid[0][c] == "."]
        return random.choice(legal) if legal else None
