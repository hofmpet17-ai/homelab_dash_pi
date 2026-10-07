from flask import Flask, render_template, redirect, request
from datetime import date, timedelta, datetime
import os
import sqlite3
import database
app = Flask(__name__)


def format_frist(frist): 
    datum = datetime.strptime(frist, "%Y-%m-%d").date()
    if datum == date.today():
        return "HEUTE"
    elif datum == (date.today()+ timedelta(days=1)): 
        return "MORGEN"
    elif datum == (date.today()+ timedelta(days=2)): 
            return "ÜBERMORGEN"
    else:
        return frist[8:10] + "." + frist[5:7] + "." + frist[0:4] 


@app.route("/")
def home(): 
    return render_template("dashboard.html")

@app.route("/wichtiges/bearbeiten/<int:task_id>", methods= ["GET","POST"])
def edit_new(task_id):
    conn = sqlite3.connect("Andis_Dash")
    if request.method =="POST":
        aktion = request.form["aktion"]
        if aktion == "speichern": 
            desc = request.form["description"]
            frist = request.form["frist"]
            if "importance" in request.form:
                imp =1 
            else: 
                imp = 0
            database.update_task(conn, task_id, desc, frist, imp)
        if aktion == "löschen":
            database.delete_task(conn, task_id)
        conn.close()
        return redirect("/wichtiges")
    # GET aufruf: 
    task = database.get_task(conn, task_id)
    conn.close()
    return render_template("bearbeiten.html",task=task)


@app.route("/wichtiges/erledigt/<int:task_id>", methods=["POST"])
def erledigt(task_id): 
    conn = sqlite3.connect("Andis_Dash")
    database.mark_done(conn, task_id)
    conn.close()
    return redirect("/wichtiges")
@app.route("/wichtiges/löschen/<int:task_id>", methods =["POST"])
def remove(task_id):
    conn = sqlite3.connect("Andis_Dash")
    database.delete_task(conn,task_id)
    conn.close()
    return redirect("/wichtiges") 
@app.route("/wichtiges/unerledigt/<int:task_id>", methods=["POST"])
def unerledigt(task_id): 
    conn = sqlite3.connect("Andis_Dash")
    database.mark_undone(conn, task_id)
    conn.close()
    return redirect("/wichtiges")
#@app.route("/wichtiges/bearbeiten/<int:task_id>")
#def edit(task_id):
 #   conn = sqlite3.connect("Andis_Dash")
  #  task = database.get_task(conn,task_id)
   # conn.close()
    #return render_template("bearbeiten.html", task = task)

@app.route("/wichtiges", methods=["GET", "POST"])
def create(): 
    conn = sqlite3.connect("Andis_Dash")
    if request.method =="POST":
        description = request.form["description"]
        frist = request.form["frist"]
        if "importance" in request.form: 
            importance = 1 
        else:
            importance = 0
        database.insert_data(conn,description,frist,importance)
    
    sortierung = request.args.get("sortierung")

    open= database.get_open_tasks(conn,sortierung)
    done= database.get_done_tasks(conn)
    conn.close()
    return render_template("wichtiges.html", open = open, done = done, format_frist = format_frist)

if not os.path.exists("Andis_Dash"):
    database.create_db("Andis_Dash")
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)