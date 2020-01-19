#!/usr/bin/env python3
# Developer : Hamdy Abou El Anein
# hamdy.aea@protonmail.com


import easygui_qt as easy
import sqlite3


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
    c.execute("INSERT INTO repas VALUES (?, ?);", (date, "Repas Shérine"))
    conn.commit()
    conn.close()


def Read():
    conn = sqlite3.connect("garde.db")
    c = conn.cursor()
    c.execute("SELECT * FROM repas")
    print(c.fetchall())
    conn.commit()
    conn.close()


def Delete():
    conn = sqlite3.connect("garde.db")
    c = conn.cursor()
    sql_delete_query = """DELETE from repas where date = '2020-01-28'"""
    c.execute(sql_delete_query)
    conn.commit()
    c.execute("SELECT * FROM repas")
    print(c.fetchall())
    conn.commit()
    conn.close()


# Delete()
# main()
Read()
