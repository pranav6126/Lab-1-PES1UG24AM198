import random


class AI:
    def _wins(self, board, col, token):
        trial = board.copy()
        return trial.drop(col, token) is not None and trial.winner(token)

    def choose_column(self, board, me="O", opponent="X"):
        legal = board.legal_columns()
        if not legal:
            return None

        # 1. Take an immediate win
        for col in legal:
            if self._wins(board, col, me):
                return col

        # 2. Block an immediate player win
        for col in legal:
            if self._wins(board, col, opponent):
                return col

        # 3. Avoid moves that hand the opponent a win on top of ours
        safe = []
        for col in legal:
            trial = board.copy()
            trial.drop(col, me)
            if not any(self._wins(trial, c, opponent) for c in trial.legal_columns()):
                safe.append(col)
        pool = safe or legal

        # 4. Prefer the centre columns
        best = min(abs(c - 3) for c in pool)
        return random.choice([c for c in pool if abs(c - 3) == best])
