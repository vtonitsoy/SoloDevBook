import sqlite3

DB_NAME = 'solodevbook.db'

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # чтобы в read запросах получать row по ключу (типо не [1], а ['name'])
    return conn

def init_statuses_once():
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("SELECT name FROM statuses")
    existing = set(name for (name,) in cur.fetchall())

    default_statuses = ["Backlog", "To Do", "In Progress", "Done"]

    for status in default_statuses:
        if status not in existing:
            cur.execute("INSERT INTO statuses(name) VALUES(?)", (status,))
    
    conn.commit()
    conn.close()

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
        FOREIGN KEY (status_id) REFERENCES statuses(id) ON DELETE CASCADE,
        FOREIGN KEY (sprint_id) REFERENCES sprints(id) ON DELETE CASCADE
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
        to_drop TEXT NOT NULL,
        try TEXT NOT NULL
    )   
"""
    )
    init_statuses_once()
    conn.commit()
    conn.close()



def add_sprint(name, start_date, end_date,description=None):
    conn = get_db()
    cur = conn.cursor()
    if description:
        cur.execute(
            "INSERT INTO sprints(name, description, start_date, end_date) VALUES(?, ?, ?, ?)",
            (name, description, start_date, end_date)
        )
    else:
        cur.execute(
            "INSERT INTO sprints(name, start_date, end_date) VALUES(?, ?, ?)",
            (name, start_date, end_date)
        )
    conn.commit()
    conn.close()

def add_task(name, description, created_at, status_id, sprint_id):
    conn = get_db()
    cur = conn.cursor()
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

def add_retro(topic, date, keep, to_drop, try_, description=None):
    conn = get_db()
    cur = conn.cursor()
    if description:
        cur.execute(
            "INSERT INTO retro(topic, description, date, keep, to_drop, try) VALUES(?, ?, ?, ?, ?, ?)",
            (topic, description, date, keep, to_drop, try_)
        )
    else:
        cur.execute(
            "INSERT INTO retro(topic, date, keep, to_drop, try) VALUES(?, ?, ?, ?, ?)",
            (topic, date, keep, to_drop, try_)
        )
    conn.commit()
    conn.close()


def update_sprint(sprint_id, name=None, start_date=None, end_date=None, description=None):
    conn = get_db()
    cur = conn.cursor()
    fields = []
    values = []
    if name is not None:
        fields.append("name = ?")
        values.append(name)
    if start_date is not None:
        fields.append("start_date = ?")
        values.append(start_date)
    if end_date is not None:
        fields.append("end_date = ?")
        values.append(end_date)
    if description is not None:
        fields.append("description = ?")
        values.append(description)
    if fields:
        query = f"UPDATE sprints SET {', '.join(fields)} WHERE id = ?"
        values.append(sprint_id)
        cur.execute(query, values)
        conn.commit()
    conn.close()

def update_task(task_id, name=None, description=None, created_at=None, status_id=None, sprint_id=None):
    conn = get_db()
    cur = conn.cursor()
    fields = []
    values = []
    if name is not None:
        fields.append("name = ?")
        values.append(name)
    if description is not None:
        fields.append("description = ?")
        values.append(description)
    if created_at is not None:
        fields.append("created_at = ?")
        values.append(created_at)
    if status_id is not None:
        fields.append("status_id = ?")
        values.append(status_id)
    if sprint_id is not None:
        fields.append("sprint_id = ?")
        values.append(sprint_id)
    if fields:
        query = f"UPDATE tasks SET {', '.join(fields)} WHERE id = ?"
        values.append(task_id)
        cur.execute(query, values)
        conn.commit()
    conn.close()

def update_standup(standup_id, done=None, todo=None, blockers=None, date=None):
    conn = get_db()
    cur = conn.cursor()
    fields = []
    values = []
    if done is not None:
        fields.append("done = ?")
        values.append(done)
    if todo is not None:
        fields.append("todo = ?")
        values.append(todo)
    if blockers is not None:
        fields.append("blockers = ?")
        values.append(blockers)
    if date is not None:
        fields.append("date = ?")
        values.append(date)
    if fields:
        query = f"UPDATE standups SET {', '.join(fields)} WHERE id = ?"
        values.append(standup_id)
        cur.execute(query, values)
        conn.commit()
    conn.close()

def update_retro(retro_id, topic=None, description=None, date=None, keep=None, to_drop=None, try_=None):
    conn = get_db()
    cur = conn.cursor()
    fields = []
    values = []
    if topic is not None:
        fields.append("topic = ?")
        values.append(topic)
    if description is not None:
        fields.append("description = ?")
        values.append(description)
    if date is not None:
        fields.append("date = ?")
        values.append(date)
    if keep is not None:
        fields.append("keep = ?")
        values.append(keep)
    if to_drop is not None:
        fields.append("to_drop = ?")
        values.append(to_drop)
    if try_ is not None:
        fields.append("try = ?")
        values.append(try_)
    if fields:
        query = f"UPDATE retro SET {', '.join(fields)} WHERE id = ?"
        values.append(retro_id)
        cur.execute(query, values)
        conn.commit()
    conn.close()

def get_all_statuses():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM statuses")
    result = cur.fetchall()
    conn.close()
    return result

def get_all_sprints():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM sprints")
    result = cur.fetchall()
    conn.close()
    return result

def get_all_tasks():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks")
    result = cur.fetchall()
    conn.close()
    return result

def get_tasks_by_sprint(sprint_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks WHERE sprint_id = ?", (sprint_id,))
    result = cur.fetchall()
    conn.close()
    return result

def get_all_standups():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM standups")
    result = cur.fetchall()
    conn.close()
    return result

def get_all_retro():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM retro")
    result = cur.fetchall()
    conn.close()
    return result


def delete_status(status_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM statuses WHERE id = ?", (status_id,))
    conn.commit()
    conn.close()

def delete_sprint(sprint_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM sprints WHERE id = ?", (sprint_id,))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

def delete_standup(standup_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM standups WHERE id = ?", (standup_id,))
    conn.commit()
    conn.close()

def delete_retro(retro_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM retro WHERE id = ?", (retro_id,))
    conn.commit()
    conn.close()
