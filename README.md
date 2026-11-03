# Garde et repas

Developer: Hamdy Abou El Anein — hamdy.aea@protonmail.com

Local Tkinter meal register using Python 3 and SQLite. No external Python dependencies.

Run `python3 garde.py`. New data is stored under `$XDG_DATA_HOME/garde-repas/garde.db` (default `~/.local/share`). To use an existing database explicitly, run `python3 garde.py --database /path/to/garde.db`. Back up that file first. The historical `repas(date, repas)` schema is preserved; no existing database is automatically moved or overwritten.

Dates use YYYY-MM-DD. Multiple meals on a date are supported; deletion affects only selected rows and requires confirmation.

Run `python3 -m unittest -v`. Tests use temporary databases, never personal records.
