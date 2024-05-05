# id: 0, name: 1, description: 2, obstacles: 3, selected: 4, grid_rows: 5, grid_columns: 6, time_interval: 7

def ADD_CONFIG(parameters):
    return ("INSERT INTO CONFIGS (name, description, obstacles, selected, grid_rows, grid_columns, time_interval) VALUES (?,?,?,?,?,?,?)", parameters)

def SET_SELECTED(parameters):
    return ("UPDATE CONFIGS SET selected = 1 WHERE id = ?", parameters)

def DELETE_CONFIG(parameters):
    return ("DELETE FROM CONFIGS WHERE id = ?", (parameters))

def SELECT(field, condition_field, condition_value):
    return ("SELECT {} FROM CONFIGS WHERE {} = ?".format(field, condition_field), (str(condition_value)))

def UPDATE(field, value, id):
    return ('UPDATE CONFIGS SET {} = "{}" WHERE id = ?'.format(field, value), id)

CREATE_TABLE = ("CREATE TABLE IF NOT EXISTS CONFIGS (id INTEGER PRIMARY KEY, name TEXT, description TEXT, obstacles TEXT, selected BOOLEAN, grid_rows INTEGER, grid_columns INTEGER, time_interval INTEGER)", ())
RESET_SELECTED = ("UPDATE CONFIGS SET selected = 0", ())
NEW_CONFIG_SET_SELECTED = ("UPDATE CONFIGS SET selected = 1 WHERE id = (SELECT MAX(id) FROM CONFIGS)", ())
SELECT_SELECTED_CONFIGS = ("SELECT * FROM CONFIGS WHERE selected = 1", ())
SELECT_ALL_CONFIGS = ("SELECT * FROM CONFIGS", ())