from flask import Flask, render_template, request, redirect
import os
import datetime

import db

app = Flask(__name__)


def initialize_db():
    if not os.path.exists(db.DB_NAME):
        db.init_db()
    else:
        try:
            conn = db.get_db()
            conn.execute("SELECT 1 FROM statuses LIMIT 1;")
        except Exception:
            db.init_db()
        finally:
            conn.close()


@app.route("/")
def index():
    sprints = db.get_all_sprints()
    print(sprints)
    return render_template("index.html", sprints=sprints)

@app.route("/add_sprint", methods=['GET', 'POST'])
def add_sprint():
    if request.method == "POST":
        name = request.form["name"]
        description = request.form.get("description", None)
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        db.add_sprint(name, description, start_date, end_date)
        return redirect("/")
    return render_template("add_sprint.html")

@app.route("/sprint<int:id>")
def sprint(id):
    sprint = db.get_sprint_by_id(id)
    tasks = db.get_tasks_by_sprint(id)
    statuses = db.get_all_statuses()
    return render_template("sprint.html", sprint=sprint, tasks=tasks, statuses=statuses)

@app.route("/sprint<int:sprint_id>/add_task", methods=['GET', 'POST'])
def add_task(sprint_id):
    if request.method == "POST":
        name = request.form["name"]
        description = request.form.get("description", None)
        status = int(request.form["status"])
        created_at = datetime.datetime.now()
        db.add_task(name,description,created_at,status,sprint_id)
        return redirect(f"/sprint{sprint_id}")
    else:
        statuses = db.get_all_statuses()
        return render_template("add_task.html", statuses=statuses, sprint_id=sprint_id)

initialize_db()
app.run(debug=True)
