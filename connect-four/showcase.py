"""Terminal showcase for the video. Works on BOTH the original and the fixed code.
Usage: python3 showcase.py before   |   python3 showcase.py after
Set SPEED=0 to run instantly (e.g. SPEED=0 python3 showcase.py after)."""
import os
import sys
import time
from unittest.mock import patch

from board import Board, ROWS, COLS
from ai import AI
from game import Game

LABEL = sys.argv[1].upper() if len(sys.argv) > 1 else "RUN"
SPEED = float(os.environ.get("SPEED", "1"))
GREEN, RED, BOLD, END = "\033[92m", "\033[91m", "\033[1m", "\033[0m"


def pause(s):
    time.sleep(s * SPEED)


def show(name, ok):
    tag = f"{GREEN}PASS{END}" if ok else f"{RED}FAIL{END}"
    print(f"  [{tag}] {name}")
    pause(0.15)


def title(text):
    print(f"\n{BOLD}{text}{END}")
    pause(0.4)


def build(moves):
    b = Board()
    for col, tok in moves:
        b.drop(col, tok)
    return b


print(f"{BOLD}===== CONNECT FOUR: {LABEL} CHANGES ====={END}")
pause(0.5)

# ---------------- Task 1 ----------------
title("TASK 1: win detection (all four directions)")
horiz = build([(c, "X") for c in range(4)])
vert = build([(2, "X")] * 4)
diag_up = build([(0,"X"),(1,"O"),(1,"X"),(2,"O"),(6,"X"),(2,"O"),(2,"X"),
                 (3,"O"),(6,"X"),(3,"O"),(5,"X"),(3,"O"),(3,"X")])
diag_dn = build([(6,"X"),(5,"O"),(5,"X"),(4,"O"),(0,"X"),(4,"O"),(4,"X"),
                 (3,"O"),(0,"X"),(3,"O"),(1,"X"),(3,"O"),(3,"X")])
three = build([(c, "X") for c in range(3)])
show("horizontal four  -> win", horiz.winner("X"))
show("vertical four    -> win", vert.winner("X"))
show("diagonal  /  four -> win", diag_up.winner("X"))
show("diagonal  \\  four -> win", diag_dn.winner("X"))
show("only three in a row -> NOT a win", not three.winner("X"))
print("  Board with a '/' diagonal for X:")
diag_up.print()
pause(1.0)

# ---------------- Task 2 ----------------
title("TASK 2: terminal states and invalid moves")
b = Board()
before = [r[:] for r in b.grid]
for bad in (-1, 7, 99):
    b.drop(bad, "X")
show("out-of-range columns leave board unchanged", b.grid == before)

b = Board()
for i in range(ROWS):
    b.drop(0, "X" if i % 2 else "O")
snap = [r[:] for r in b.grid]
res = b.drop(0, "X")
show("dropping into a FULL column is rejected and board unchanged",
     res is None and b.grid == snap)

draw = Board()
a, c = "XXOOXXO", "OOXXOOX"
draw.grid = [list(a if r % 2 == 0 else c) for r in range(ROWS)]
show("full board with no winner is a DRAW",
     draw.full() and not draw.winner("X") and not draw.winner("O"))
pause(0.5)

# ---------------- Task 3 ----------------
title("TASK 3: AI decisions (30 trials each)")
N = 30
win_pos = build([(0,"O"),(1,"O"),(2,"O"),(6,"X"),(6,"X")])
block_pos = build([(0,"X"),(1,"X"),(2,"X"),(5,"O")])
wins = sum(AI().choose_column(win_pos) == 3 for _ in range(N))
blocks = sum(AI().choose_column(block_pos) == 3 for _ in range(N))
full_col = Board()
for i in range(ROWS):
    full_col.drop(3, "X" if i % 2 else "O")
legal_ok = all(AI().choose_column(full_col) not in (3, None) for _ in range(N))
print(f"  AI took the immediate win   : {wins}/{N}")
show("AI always takes an immediate win", wins == N)
print(f"  AI blocked the player's win : {blocks}/{N}")
show("AI always blocks an immediate player win", blocks == N)
show("AI never picks a full column", legal_ok)
pause(0.5)

# ---------------- Tasks 2 + 4 live game ----------------
title("TASKS 2 + 4: live game (scripted input: abc, 9, then moves)")
script = iter(["abc", "9", "0", "1", "2", "7", "3", "7", "6", "4"])
ai_moves = iter([1, 2, 2, 3, 3, 3])


class StubAI:
    def choose_column(self, board, me="O", opponent="X"):
        return next(ai_moves, 4)


def fake_input(prompt=""):
    try:
        val = next(script)
    except StopIteration:
        print(f"  {RED}!! game asked for ANOTHER turn after the winning move{END}")
        return "q"
    print(f"  > you type: {val}")
    pause(0.35)
    return val


g = Game()
g.ai = StubAI()
with patch("builtins.input", fake_input), patch.object(Board, "print", lambda self: None):
    g.run()
print("  Final board:")
g.board.print()
pause(0.8)

# ---------------- quit ----------------
title("QUIT handling")
with patch("builtins.input", lambda p="": "q"):
    Game().run()
print(f"\n{BOLD}===== END OF {LABEL} DEMO ====={END}")
