import unittest
from unittest.mock import patch
from board import Board, ROWS, COLS
from ai import AI
from game import Game


def place(board, moves):
    for col, tok in moves:
        board.drop(col, tok)


class TestWins(unittest.TestCase):
    def test_horizontal(self):
        b = Board(); place(b, [(c, "X") for c in range(4)])
        self.assertTrue(b.winner("X"))

    def test_vertical(self):
        b = Board(); place(b, [(2, "X")] * 4)
        self.assertTrue(b.winner("X"))

    def test_diagonal_up(self):
        b = Board()
        place(b, [(0,"X"),(1,"O"),(1,"X"),(2,"O"),(6,"X"),(2,"O"),(2,"X"),
                  (3,"O"),(6,"X"),(3,"O"),(5,"X"),(3,"O"),(3,"X")])
        self.assertTrue(b.winner("X"))

    def test_diagonal_down(self):
        b = Board()
        place(b, [(6,"X"),(5,"O"),(5,"X"),(4,"O"),(0,"X"),(4,"O"),(4,"X"),
                  (3,"O"),(0,"X"),(3,"O"),(1,"X"),(3,"O"),(3,"X")])
        self.assertTrue(b.winner("X"))

    def test_three_is_not_a_win(self):
        b = Board(); place(b, [(c, "X") for c in range(3)])
        self.assertFalse(b.winner("X"))


class TestBoardEdges(unittest.TestCase):
    def test_draw(self):
        b = Board()
        a, c = "XXOOXXO", "OOXXOOX"
        b.grid = [list(a if r % 2 == 0 else c) for r in range(ROWS)]
        self.assertTrue(b.full())
        self.assertFalse(b.winner("X"))
        self.assertFalse(b.winner("O"))

    def test_full_column_rejected(self):
        b = Board()
        for i in range(ROWS):
            self.assertIsNotNone(b.drop(0, "X" if i % 2 else "O"))
        before = [r[:] for r in b.grid]
        self.assertIsNone(b.drop(0, "X"))
        self.assertEqual(b.grid, before)

    def test_invalid_columns_do_not_change_board(self):
        b = Board(); before = [r[:] for r in b.grid]
        for bad in (-1, 7, 99):
            self.assertIsNone(b.drop(bad, "X"))
        self.assertEqual(b.grid, before)


class TestAI(unittest.TestCase):
    def test_takes_win(self):
        b = Board(); place(b, [(0,"O"),(1,"O"),(2,"O"),(6,"X"),(6,"X")])
        self.assertEqual(AI().choose_column(b), 3)

    def test_blocks_win(self):
        b = Board(); place(b, [(0,"X"),(1,"X"),(2,"X"),(5,"O")])
        self.assertEqual(AI().choose_column(b), 3)

    def test_never_picks_full_column(self):
        b = Board()
        for i in range(ROWS):
            b.drop(3, "X" if i % 2 else "O")
        for _ in range(200):
            self.assertNotEqual(AI().choose_column(b), 3)

    def test_no_legal_moves(self):
        b = Board()
        b.grid = [list("XXOOXXO") for _ in range(ROWS)]
        self.assertIsNone(AI().choose_column(b))


class TestGame(unittest.TestCase):
    @patch("builtins.input", side_effect=["abc", "0", "9", "q"])
    def test_invalid_input_then_quit(self, _):
        g = Game(); g.run()
        self.assertTrue(all(c == "." for row in g.board.grid for c in row))

    @patch("builtins.input", side_effect=["q"])
    def test_quit(self, _):
        self.assertIsNone(Game().run())

    @patch("builtins.print")
    @patch("builtins.input", side_effect=["1"])
    def test_feedback_once_per_move(self, _, mock_print):
        g = Game()
        g.ai.choose_column = lambda *a, **k: 1
        with self.assertRaises(StopIteration):
            g.run()
        placed = [c for c in mock_print.call_args_list if "placed a disc" in str(c)]
        self.assertEqual(len(placed), 2)  # one for X, one for O

    @patch("builtins.input", side_effect=["1", "2", "3", "4", "5"])
    def test_win_stops_game_before_next_turn(self, mock_in):
        g = Game()
        cols = iter([0, 0, 0])
        g.ai.choose_column = lambda *a, **k: next(cols)
        # X plays 1,2,3,4 on the bottom row -> wins on 4th input
        g.run()
        self.assertEqual(mock_in.call_count, 4)


if __name__ == "__main__":
    unittest.main()
