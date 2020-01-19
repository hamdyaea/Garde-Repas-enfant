#!/usr/bin/env python3
# Developer : Hamdy Abou El Anein
# hamdy.aea@protonmail.com

# To delete a value use db browser for sqlite

import easygui_qt as easy
import sqlite3
import sys


def Selector():
    choices = ["New RDV", "Read all RDV", "New Database"]
    reply = easy.get_choice("What is the best Python implementation", choices=choices)
    if reply == "New Database":
        NewDb()
    elif reply == "New RDV":
        main()
    elif reply == "Read all RDV":
        Read()
    else:
        sys.exit(0)


def NewDb():
    conn = sqlite3.connect("garde.db")
    c = conn.cursor()
    c.execute(
        """CREATE TABLE repas
                 (date text, repas text)"""
    )
    conn.commit()
    conn.close()


def main():
    conn = sqlite3.connect("garde.db")
    c = conn.cursor()
    date = easy.get_date()
    easy.set_font_size(20)
    Message = "Add to the database the " + str(date)
    Title = "Confirm write to the database"
    easy.show_message(message=Message, title=Title)
    c.execute("INSERT INTO repas VALUES (?, ?);", (date, "Repas Enfant"))
    conn.commit()
    conn.close()


def Read():
    message = ""
    conn = sqlite3.connect("garde.db")
    c = conn.cursor()
    c.execute("SELECT * FROM repas ORDER BY date")
    # print(c.fetchall())
    Total = c.fetchall()
    for i in Total:
        message = message + str(i) + str("\n")
    conn.commit()
    conn.close()
    message = message.replace("(", " ")
    message = message.replace(")", " ")
    message = message.replace("'", " ")
    Message = message
    Title = "Liste des repas"
    easy.show_code(text=Message, title=Title)


"""
def Delete():
    message = ""
    datetodel = easy.get_date()
    date = str(datetodel)
    conn = sqlite3.connect("garde.db")
    c = conn.cursor()
    c.execute("DELETE FROM repas where date=(?);", (date))
    conn.commit()
    c.execute("SELECT * FROM repas ORDER BY date")
    Total = c.fetchall()
    for i in Total:
        message = message + str(i) + str("\n")
    conn.commit()
    conn.close()
    message = message.replace("(", " ")
    message = message.replace(")", " ")
    message = message.replace("'", " ")
    Message = message
    Title = "Liste des repas"
    easy.show_code(text=Message, title=Title)
"""

Selector()
