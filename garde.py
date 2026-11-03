#!/usr/bin/env python3
# Developer: Hamdy Abou El Anein
# Contact: hamdy.aea@protonmail.com
"""Local meal register; existing two-column SQLite databases remain compatible."""
import argparse
from datetime import date
import os
from pathlib import Path
import sqlite3


def default_database():
    return Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local/share")) / "garde-repas" / "garde.db"


class MealStore:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as db:
            db.execute("CREATE TABLE IF NOT EXISTS repas (date TEXT, repas TEXT)")

    def connect(self):
        return sqlite3.connect(self.path)

    def add(self, day, description="Repas Enfant"):
        normalized = date.fromisoformat(day).isoformat()
        if not description.strip():
            raise ValueError("Le repas ne peut pas être vide.")
        with self.connect() as db:
            db.execute("INSERT INTO repas VALUES (?, ?)", (normalized, description.strip()))

    def all(self):
        with self.connect() as db:
            return db.execute("SELECT rowid, date, repas FROM repas ORDER BY date, rowid").fetchall()

    def delete(self, row_id):
        with self.connect() as db:
            return db.execute("DELETE FROM repas WHERE rowid = ?", (row_id,)).rowcount


def main(argv=None):
    parser = argparse.ArgumentParser(description="Registre local des repas")
    parser.add_argument("--database", type=Path, default=default_database(),
                        help="Base SQLite existante ou nouvelle (aucune migration automatique)")
    args = parser.parse_args(argv)
    import tkinter as tk
    from tkinter import messagebox, ttk
    root = tk.Tk()
    root.title("Garde et repas")
    try:
        store = MealStore(args.database)
    except (OSError, sqlite3.Error) as exc:
        messagebox.showerror("Base de données", str(exc), parent=root)
        root.destroy()
        return 1
    frame = ttk.Frame(root, padding=16)
    frame.pack(fill="both", expand=True)
    ttk.Label(frame, text="Date (AAAA-MM-JJ)").pack(anchor="w")
    day = ttk.Entry(frame)
    day.insert(0, date.today().isoformat())
    day.pack(fill="x")
    table = ttk.Treeview(frame, columns=("date", "repas"), show="headings")
    table.heading("date", text="Date")
    table.heading("repas", text="Repas")
    table.pack(fill="both", expand=True, pady=10)

    def refresh():
        table.delete(*table.get_children())
        for row_id, meal_day, meal in store.all():
            table.insert("", "end", iid=str(row_id), values=(meal_day, meal))

    def add():
        try:
            store.add(day.get())
            refresh()
        except (ValueError, sqlite3.Error) as exc:
            messagebox.showerror("Ajout impossible", str(exc), parent=root)

    def remove():
        selected = table.selection()
        if selected and messagebox.askyesno("Confirmer", "Supprimer les repas sélectionnés ?", parent=root):
            try:
                for item in selected:
                    store.delete(int(item))
                refresh()
            except sqlite3.Error as exc:
                messagebox.showerror("Suppression impossible", str(exc), parent=root)

    ttk.Button(frame, text="Ajouter un repas", command=add).pack(fill="x")
    ttk.Button(frame, text="Supprimer la sélection", command=remove).pack(fill="x")
    ttk.Label(frame, text=str(args.database)).pack()
    refresh()
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
