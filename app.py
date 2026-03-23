from flask import Flask, render_template, request, redirect, url_for
import csv
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/display")
def display():
    tasks = []
    with open("tasks.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            tasks.append(row)
    return render_template("display.html", tasks=tasks)

@app.route("/display/<project_title>")
def display_project(project_title):
    tasks = []
    with open("tasks.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["project_title"] == project_title:
                tasks.append(row)
    return render_template("display.html", tasks=tasks, project_title=project_title)

@app.route("/input", methods=["GET", "POST"])
def input_task():
    if request.method == "POST":
        new_task = {
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "project_title": request.form["project_title"],
            "title": request.form["title"],
            "description": request.form["description"],
            "status": request.form["status"],
            "next_steps": request.form["next_steps"],
        }
        with open("tasks.csv", "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["datetime", "project_title", "title", "description", "status", "next_steps"])
            writer.writerow(new_task)
        return redirect(url_for("display"))
        if request.method == "POST":
    project_title = request.form["project_title"]
    title = request.form["title"]
    description = request.form["description"]
    status = request.form["status"]
    next_steps = request.form["next_steps"]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("tasks.csv", "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["project_title", "title", "description", "status", "next_steps", "timestamp"])
        writer.writerow({
            "project_title": project_title,
            "title": title,
            "description": description,
            "status": status,
            "next_steps": next_steps,
            "timestamp": timestamp
        })

    return redirect(url_for("display"))

    # GET block — reads existing project titles for the datalist
    project_titles = []
    with open("tasks.csv", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["project_title"] not in project_titles:
                project_titles.append(row["project_title"])

    return render_template("input.html", project_titles=project_titles)
    # Build the list of existing project titles for the datalist autocomplete
    projects = []
    seen = set()
    with open("tasks.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            t = row["project_title"]
            if t not in seen:
                projects.append(t)
                seen.add(t)
    return render_template("input.html", projects=projects)

if __name__ == "__main__":
    app.run(debug=True)
