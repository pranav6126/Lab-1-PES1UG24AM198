# Issues found in `pet_shelter.py` (original line numbers)

| # | Issue | Tool / Code | Type | Severity | Line(s) | Description | Fix Approach | Commit |
|---|-------|-------------|------|----------|---------|-------------|--------------|--------|
| 1 | SQL injection | Bandit B608 | Security | **Medium** | 10 | INSERT built with `%`-formatting from caller data; a name such as `x'); DROP TABLE pets;--` alters the query (an apostrophe in a name like `O'Malley` also breaks it) | Parameterized query with `?` placeholders; `int(age)` keeps the old `%d` integer coercion | Bandit |
| 2 | Mutable default argument | Pylint W0102 | Bug | Warning | 9 | `tags=[]` is created once and shared by every call that omits `tags` | Default `None`, create a new list inside the function | Pylint |
| 3 | Bare `except:` | Pylint W0702, Flake8 E722 | Bug / Style | Warning | 29 | Catches everything incl. `KeyboardInterrupt`; was also hiding the empty-table case (`row[0]` on `None`) | Explicit `row is None` check; catch only `sqlite3.Error` and log it | Pylint |
| 4 | Silent swallowed exception | Bandit B110, Pylint W0718 | Security / Quality | Low | 35-37 | `except Exception: pass` hides DB failures when clearing records | Catch `sqlite3.Error` and log with `LOGGER.exception` | Bandit |
| 5 | Weak PRNG for codes | Bandit B311 | Security | Low | 22 | `random.randint` is predictable; adoption codes are issued tokens | `secrets.randbelow(9000) + 1000` (same 1000-9999 range) | Bandit |
| 6 | `global` statement / constant naming | Pylint W0603, C0103 | Design | Warning | 6, 16 | Mutable module state rebound via `global`; lower-case "constant" | Counter kept in `ADOPTION_STATS` dict (no rebinding) | Pylint |
| 7 | Non-snake_case names | Pylint C0103 | Naming | Convention | 9, 21, 25, 33, 40 | `registerPet`, `adoptionCode`, `oldestAvailable`, `clearUnadopted`, `shelterStatus` | Renamed to snake_case (all call sites updated) | Pylint |
| 8 | Missing docstrings | Pylint C0114, C0116 | Documentation | Convention | 1, 9, 15, 21, 25, 33, 40, 45 | Module and all functions undocumented | Added concise docstrings | Pylint |
| 9 | Lines too long | Flake8 E501, Pylint C0301 | Style | Convention | 5, 10, 27 | 113/116/103 characters | Wrapped (implicit string concatenation, no logic change) | Flake8 |
| 10 | Multiple statements on a line | Flake8 E701, Pylint C0321 | Style | Convention | 41 | `if ...: return "active"` | Split over two lines | Flake8 |
| 11 | `%` formatting | Pylint C0209 | Style | Convention | 10 | Suggested f-string | Not applied: removed entirely by the parameterized query (an f-string would have re-introduced SQL injection) | Bandit |

## Notes on decisions
- Nothing was suppressed (`# noqa`, `# nosec`, `# pylint: disable`); every finding was fixed in code.
- E722 (Flake8) was resolved in the Pylint commit and W0718 (Pylint) in the Bandit commit because one code change fixes the finding in both tools.
- `main()` is still invoked at import time and the module-level `conn` is kept, as in the original; changing that is outside this lab's scope.
