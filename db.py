import sqlite3

DB_NAME = 'solodevbook.db'

def get_db():
    conn = sqlite3.connect(DB_NAME)
    #conn.row_factory = sqlite3.Row  # зачем вообще это мне?
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.executescript(
    """
    CREATE TABLE IF NOT EXISTS statuses(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS sprints(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        start_date DATE NOT NULL,
        end_date DATE NOT NULL
    );
    CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        created_at DATE NOT NULL,
        status_id INTEGER NOT NULL,
        sprint_id INTEGER NOT NULL,
        FOREIGN KEY (status_id) REFERENCES statuses(id),
        FOREIGN KEY (sprint_id) REFERENCES sprints(id)
    );
    CREATE TABLE IF NOT EXISTS standups(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        done TEXT NOT NULL,
        todo TEXT NOT NULL,
        blockers TEXT NOT NULL,
        date DATE NOT NULL
    );
    CREATE TABLE IF NOT EXISTS retro(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT NOT NULL,
        description TEXT,
        date DATE NOT NULL
        keep  TEXT NOT NULL,
        drop TEXT NOT NULL,
        try TEXT NOT NULL
    )   
"""
    )
    conn.commit()
    conn.close()

def add_sprint(name, description, start_date, end_date):
    conn = get_db()
    cur = conn.cursor()
    # будет ли работать если нет description?
    cur.execute(
        "INSERT INTO sprints(name, description, start_date, end_date) VALUES(?, ?, ?, ?)",
        (name, description, start_date, end_date)
    )
    conn.commit()
    conn.close()

def add_task(name, description, created_at, status_id, sprint_id):
    conn = get_db()
    cur = conn.cursor()
    # будет ли работать если нет description?
    cur.execute(
        "INSERT INTO tasks(name, description, created_at, status_id, sprint_id) VALUES(?, ?, ?, ?, ?)",
        (name, description, created_at, status_id, sprint_id)
    )
    conn.commit()
    conn.close()

def add_standup(done, todo, blockers, date):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO standups(done, todo, blockers, date) VALUES(?, ?, ?, ?)",
        (done, todo, blockers, date)
    )
    conn.commit()
    conn.close()

def add_retro(topic, description, date, keep, drop, try_):
    conn = get_db()
    cur = conn.cursor()
    # будет ли работать если нет description?
    cur.execute(
        "INSERT INTO retro(topic, description, date, keep, drop, try) VALUES(?, ?, ?, ?, ?, ?)",
        (topic, description, date, keep, drop, try_)
    )
    conn.commit()
    conn.close()
