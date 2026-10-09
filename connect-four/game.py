from board import Board, COLS, ROWS
from ai import AI


class Game:
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.turn = "X"

    def run(self):
        print("Connect Four — you are X. Enter 1-7 to drop a disc, q to quit.")
        while True:
            self.board.print()

            if self.turn == "X":
                try:
                    raw = input("Column (1-7), or q: ").strip().lower()
                except (EOFError, KeyboardInterrupt):
                    print("\nInput closed. Game ended.")
                    return
                if raw in ("q", "quit"):
                    print("You quit. Game over.")
                    return
                try:
                    col = int(raw) - 1
                except ValueError:
                    print("Invalid input: enter a number from 1 to 7, or q.")
                    continue
                if not 0 <= col < COLS:
                    print("Invalid column: choose a number from 1 to 7.")
                    continue
            else:
                col = self.ai.choose_column(self.board, me="O", opponent="X")
                if col is None:
                    print("AI has no legal move.")
                    return

            row = self.board.drop(col, self.turn)
            if row is None:
                print(f"Column {col + 1} is full. Pick another column.")
                continue

            # Task 4: feedback once per actual placement
            print(f"{self.turn} placed a disc in column {col + 1} (row {ROWS - row} from the bottom).")

            # A winning move ends the game before another turn is requested
            if self.board.winner(self.turn):
                self.board.print()
                print(f"{self.turn} wins!")
                return
            if self.board.full():
                self.board.print()
                print("Draw: the board is full.")
                return

            self.turn = "O" if self.turn == "X" else "X"
