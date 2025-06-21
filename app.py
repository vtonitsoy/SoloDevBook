from flask import Flask, render_template, request, redirect
import os

import db

app = Flask(__name__)



def initialize_database_if_needed():
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

@app.route("/add_sprint")
def add_sprint():
    if request.method == "POST":
        name = request.form["name"]
        description = request.form.get("description", None)
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        db.add_sprint(name, description, start_date, end_date)
        return redirect("/")
    return render_template("add_sprint.html")

initialize_database_if_needed()
app.run(debug=True)
