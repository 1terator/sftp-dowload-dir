import re
import sqlite3


def get_settings(path: str):
    Settings = dict()
    try:
        with open(path) as file:
            for line in file:
                line = re.sub("\n", '', line)
                position = line.find("=")
                key = line[0:position]
                Settings[key] = line[position+1:len(line)]
            return Settings
    except Exception as error:
        return {}


def create_db(db_name: str):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE info(
        fname TEXT,
        time TEXT)
        """)
    conn.commit()
    conn.close()


def insert_array_to_db(db_name: str, Report: list):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    for info in Report:
        cur.execute("""INSERT INTO info (fname, time) VALUES
           ('"""+info[0]+"""','"""+info[1]+"""')""")
        conn.commit()
    conn.close()


def read_report_db(db_name: str):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute("SELECT * FROM info")
    for values in cur.fetchall():
        print(values[0], " <---> ", values[1])
    conn.close()
