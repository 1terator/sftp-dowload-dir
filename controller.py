import sqlite3

def create_db(db_name: str):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE info(
        fname TEXT,
        time TEXT)
        """)
    conn.commit()
    conn.close()


def insert_array_to_db(conn: sqlite3.Connection, Report: list):
    cur = conn.cursor()
    for info in Report:
        cur.execute("INSERT INTO info (fname, time) VALUES ('"+info[0]+"','"+info[1]+"')")
        conn.commit()


def read_report_db(db_name: str):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute("SELECT * FROM info")
    for values in cur.fetchall():
        print(values[0], " <---> ", values[1])
    conn.close()
