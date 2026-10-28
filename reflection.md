# Reflection

> Note: the handout text supplied did not list the four reflection questions, so these answers cover the usual themes (usefulness, false positives, tool differences, process). Align headings to your handout's exact wording if needed.

**1. Which issues were the most important to fix, and why?**
The Bandit B608 SQL injection (Medium) mattered most: user-supplied strings were pasted into an INSERT statement, so a crafted pet name could change the query. Next came the mutable default `tags=[]` (state leaking between calls) and the bare `except:` (it hid a real `None`-row bug and would swallow `KeyboardInterrupt`). Style findings were cosmetic by comparison.

**2. Did the tools report any false positives or findings you chose not to fix literally?**
None had to be left unfixed. Pylint's "use an f-string" (C0209) pointed at the very line that had the SQL injection; following it literally would have been wrong, so the right fix was parameterization. B311 is context dependent (random is fine for a lottery, not for tokens); I treated adoption codes as tokens and used `secrets`.

**3. How do the three tools differ?**
Flake8 enforces PEP 8 formatting only (line length, whitespace, bare except). Pylint reviews design and quality (naming, docstrings, globals, unused code, dangerous defaults) and gives a score (3.95 to 10.00 here). Bandit looks only for security patterns (injection, weak randomness, swallowed exceptions). Their findings overlap occasionally (bare except, except/pass), but each caught something the others did not.

**4. How did static analysis help, and what are its limits?**
It found real defects in seconds without running the program and gave a measurable before/after (Pylint 3.95 to 10.00, Bandit 3 issues to 0, Flake8 5 to 0). Its limits: it cannot tell whether the program is *correct* (a clean report does not prove behavior is unchanged, so I compared old and new behavior with a small test), it can raise context-dependent warnings, and it should never be satisfied by suppressing warnings.
