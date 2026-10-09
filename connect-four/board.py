ROWS, COLS = 6, 7


class Board:
    def __init__(self):
        self.grid = [["."] * COLS for _ in range(ROWS)]

    def drop(self, col, token):
        """Drop a token. Returns the row used, or None if the move is invalid
        (column out of range or full). An invalid move never changes the grid."""
        if not isinstance(col, int) or not 0 <= col < COLS:
            return None
        for r in range(ROWS - 1, -1, -1):
            if self.grid[r][col] == ".":
                self.grid[r][col] = token
                return r
        return None

    def legal_columns(self):
        return [c for c in range(COLS) if self.grid[0][c] == "."]

    def full(self):
        return not self.legal_columns()

    def copy(self):
        clone = Board()
        clone.grid = [row[:] for row in self.grid]
        return clone

    def winner(self, token):
        # horizontal, vertical, diagonal "\", diagonal "/"
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for r in range(ROWS):
            for c in range(COLS):
                if self.grid[r][c] != token:
                    continue
                for dr, dc in directions:
                    if all(
                        0 <= r + i * dr < ROWS
                        and 0 <= c + i * dc < COLS
                        and self.grid[r + i * dr][c + i * dc] == token
                        for i in range(4)
                    ):
                        return True
        return False

    def print(self):
        print("\n  " + " ".join(str(i + 1) for i in range(COLS)))
        for row in self.grid:
            print("  " + " ".join(row))
