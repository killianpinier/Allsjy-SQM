from flask import Flask, render_template, request, jsonify, redirect
import sqlite3
from sqm import get_sqm_image
from queries import *

app = Flask(__name__)

connect = sqlite3.connect("database.db")
connect.execute("CREATE TABLE IF NOT EXISTS CONFIGS (id INTEGER PRIMARY KEY, name TEXT, description TEXT, obstacles TEXT, selected BOOLEAN, grid_rows INTEGER, grid_columns INTEGER, time_interval INTEGER)")
connect.close()

@app.route('/')       
def index(): 
    data = {}
    selected_config = get_selected_config()
    if selected_config == None:
        selected_config = "No configuration selected"
    data["selected_config"] = selected_config[1]
    return render_template("index.html", data=data)

@app.route('/run', methods=['POST'])
def button_click():
    selected_config = get_selected_config()
    if selected_config == None:
        return jsonify({"Error", "No configuration selected"})
    config = fetch(selected_config[0], "*", "id", False)
    obstacles = [int(num) for num in config[3].split(",")].sort()
    print(obstacles)
    #get_sqm_image([], config[5], config[6])
    return jsonify({"message": "Button clicked"})

@app.route('/config/select/<config_id>', methods=['POST'])
def select_config(config_id):
    queries = [RESET_SELECTED, SET_SELECTED((config_id))]
    query(queries)
    return jsonify({"message": "Config selected"})

@app.route('/config/remove/<config_id>', methods=['POST'])
def remove_config(config_id):
    queries = [DELETE_CONFIG((config_id))]
    query(queries)
    return jsonify({"message": "Config removed"})

@app.route('/images')       
def images(): 
    return render_template("images.html")

@app.route('/configs')       
def configs():
    data = fetch_all()
    return render_template("configs.html", data=data)

@app.route('/addconfig', methods=['GET','POST'])       
def add_config():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        #obstacles = [int(num) for num in request.form['clickedItems'].split(",")]
        obstacles = request.form['clickedItems']
        grid_rows = request.form['grid_rows']
        grid_columns = request.form['grid_columns']
        time_interval = request.form['time_interval']

        if time_interval == "":
            time_interval = "0"

        queries = [
            ADD_CONFIG((name, description, obstacles, True, grid_rows, grid_columns, time_interval)),
            RESET_SELECTED,
            NEW_CONFIG_SET_SELECTED
        ]
        query(queries)

        return redirect("/")
    return render_template("add_config.html")

@app.route('/updateconfig/<config_id>', methods=['GET','POST'])       
def update_config(config_id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        if request.method == 'POST':
            pass
        else:
            cursor.execute("SELECT * FROM CONFIGS WHERE id = ?", (config_id))
            record = cursor.fetchone()
            return render_template("update_config.html", config=record)
        

@app.route('/test')
def test():
    return render_template("test.html")

def get_selected_config():
    configs = fetch(1, "*", "selected", True)
    if len(configs) > 1:
        queries = [RESET_SELECTED]
        query(queries)
    elif len(configs) == 1:
        return configs[0]
    return None

def query(queries):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        for query in queries:
            print(query[0], " -- ", query[1])
            cursor.execute(query[0], query[1])
        conn.commit()

def fetch(value, field, condition_field, fetch_all):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        query = SELECT(value, field, condition_field)
        print(query)
        cursor.execute(query[0], query[1])
        if fetch_all:
            return cursor.fetchall()
        return cursor.fetchone()

def fetch_all():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute(SELECT_ALL_CONFIGS[0])
        data = cursor.fetchall()
        return data
    
    
if __name__=='__main__': 
    app.run(port=5000, debug=True)
    #app.run(host='192.168.0.32', port=5000, debug=True)
