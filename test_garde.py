# Developer: Hamdy Abou El Anein
# Contact: hamdy.aea@protonmail.com
import sqlite3
import tempfile
from pathlib import Path
import unittest
from garde import MealStore


class MealTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "garde.db"
        self.store = MealStore(self.path)

    def test_persistence(self):
        self.store.add("2026-11-03")
        self.assertEqual(MealStore(self.path).all()[0][1:], ("2026-11-03", "Repas Enfant"))

    def test_invalid_date_does_not_write(self):
        for day in ("invalid", "2026-02-30", ""):
            with self.assertRaises(ValueError):
                self.store.add(day)
        self.assertEqual(self.store.all(), [])

    def test_delete_only_selected_record(self):
        self.store.add("2026-11-03")
        self.store.add("2026-11-03")
        self.assertEqual(self.store.delete(self.store.all()[0][0]), 1)
        self.assertEqual(len(self.store.all()), 1)

    def test_existing_schema_preserved(self):
        with sqlite3.connect(self.path) as db:
            db.execute("INSERT INTO repas VALUES ('2020-01-01', 'historique')")
        self.assertEqual(MealStore(self.path).all()[0][1:], ("2020-01-01", "historique"))

    def test_description_is_data(self):
        text = "repas'); DROP TABLE repas; --"
        self.store.add("2026-11-03", text)
        self.assertEqual(self.store.all()[0][2], text)


if __name__ == "__main__":
    unittest.main()
