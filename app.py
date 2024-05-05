from flask import Flask, render_template, request, jsonify, redirect
import sqlite3
from sqm import get_sqm_image
from queries import *

app = Flask(__name__)

DATABASE_NAME = "database.db"

class Config:
    def __init__(self, data) -> None:
        self.name = data['name']
        self.description = data['description']
        self.obstacles = data['clickedItems']
        self.selected = True
        self.grid_rows = data['grid_rows']
        self.grid_columns = data['grid_columns']
        self.time_interval = data['time_interval']
    
    def to_tuple(self):
        return (self.name, self.description, self.obstacles, self.selected, self.grid_rows, self.grid_columns, self.time_interval)

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
    config = fetch("*", "id", selected_config[0], False)
    obstacles = [int(num) for num in config[3].split(",")].sort()
    get_sqm_image(obstacles, config[5], config[6])
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
    data = fetch_all_configs()
    return render_template("configs.html", data=data)

@app.route('/addconfig', methods=['GET','POST'])       
def add_config():
    if request.method == 'POST':
        config = Config(request.form)

        if config.time_interval == "":
            config.time_interval = "0"

        queries = [
            ADD_CONFIG(config.to_tuple()),
            RESET_SELECTED,
            NEW_CONFIG_SET_SELECTED
        ]
        query(queries)

        return redirect("/")
    return render_template("add_config.html")

@app.route('/updateconfig/<config_id>', methods=['GET','POST'])       
def update_config(config_id):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        if request.method == 'POST':
            queries = [
                UPDATE("name", request.form["name"], config_id),
                UPDATE("description", request.form["description"], config_id),
                UPDATE("time_interval", request.form["time_interval"], config_id),
            ]
            query(queries)
            return redirect("/configs")
        else:
            cursor.execute("SELECT * FROM CONFIGS WHERE id = ?", (config_id))
            record = cursor.fetchone()
            return render_template("update_config.html", config=record)
        

@app.route('/test')
def test():
    return render_template("test.html")

def get_selected_config():
    configs = fetch("*", "selected", 1, True)
    if len(configs) > 1:
        queries = [RESET_SELECTED]
        query(queries)
    elif len(configs) == 1:
        return configs[0]
    return None


# ----- DATABASE management

# query: takes a list of queries as a parameter. Each element of this query is a tuple which is then passed
#        to the sqlite3 execute function. 
def query(queries):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        for query in queries:
            print(query[0], " -- ", query[1])
            cursor.execute(query[0], query[1])
        conn.commit()

# fetch: runs a fetch query with the possibility to fetch one, or all returned queries (fetch_all paramater: Bool)
def fetch(field, condition_field, condition_value, fetch_all):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        query = SELECT(field, condition_field, condition_value)
        cursor.execute(query[0], query[1])
        if fetch_all:
            return cursor.fetchall()
        return cursor.fetchone()

def fetch_all_configs():
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(SELECT_ALL_CONFIGS[0])
        data = cursor.fetchall()
        return data
    

# ----- Program entry
    
if __name__=='__main__': 
    query([CREATE_TABLE])
    app.run(port=5000, debug=False)
    #app.run(host='192.168.0.32', port=5000, debug=True)
