import sqlite3 

def create_db(conn):
    conn.execute("CREATE TABLE IF NOT EXISTS tasks \
                 (id INTEGER PRIMARY KEY, description TEXT NOT NULL, \
                    frist TEXT NOT NULL, \
                     importance  BOOLEAN NOT NULL DEFAULT 0, \
                     done  BOOLEAN NOT NULL DEFAULT 0);")
    conn.commit() 

def insert_data (conn,description,frist = 0, importance = 0): 
    try:
        
        conn.execute("INSERT INTO tasks (description,frist,importance) \
                    VALUES(?,?,?)",(description, frist, importance)) 
        conn.commit()
    except TypeError: 
        return "WRONG PARAMETERS"

def get_data(conn): 
    cursor1 = conn.execute("SELECT * FROM tasks")
    for element in cursor1: 
        print(element)
    
def delete_task(conn, id: int):
    try:
         cursor = conn.execute(" DELETE FROM tasks WHERE id = ?",(id,))
         conn.commit()
         return bool(cursor.rowcount)     
    except sqlite3.Error: 
        return False

def mark_done(conn, id): 
    try: 
        cursor = conn.execute(f"UPDATE tasks SET done  = ? WHERE id = ?", (1,id))
        conn.commit()
        return bool(cursor.rowcount)
    except sqlite3.Error: 
        return False 

def mark_undone(conn, id): 
    try: 
        cursor = conn.execute(f"UPDATE tasks SET done  = ? WHERE id = ?", (0,id))
        conn.commit()
        return bool(cursor.rowcount)
    except sqlite3.Error: 
        return False 


def update_task(conn, id, description, frist, imp): 
    try: 
        conn.execute("UPDATE tasks SET description = ?, frist = ?, importance = ?\
                              WHERE id = ?",(description, frist, imp, id))
        conn.commit()
        return True 
    except sqlite3.Error:
        return False
    

def clear_data(conn):
    cursor = conn.execute("DELETE FROM tasks")
    conn.commit()
    return bool(cursor.rowcount)
def dash_tasks(conn): 
    cursor = conn.execute("SELECT * FROM tasks WHERE importance = 1 AND\
                           done = 0 ORDER BY id DESC LIMIT 3")
    my_list = []
    for element in cursor: 
        my_list.append(element)
    return my_list

def get_open_tasks(conn, sortierung): 
    if sortierung== "frist": 
        cursor1 = conn.execute("SELECT * FROM tasks WHERE done =?\
                           ORDER BY frist",(0,))
    elif sortierung == "wichtig":
        cursor1 =conn.execute("SELECT * FROM tasks WHERE done = ?\
                              ORDER BY importance",(0,))
    else: 
        cursor1 = conn.execute("SELECT * FROM tasks WHERE done = ?",(0,))
    return cursor1.fetchall()
def get_done_tasks(conn): 
    cursor1 = conn.execute("SELECT * FROM tasks WHERE done =?",(1,))
    return cursor1.fetchall()
def get_task(conn, id): 
    cursor1= conn.execute("SELECT * FROM tasks WHERE id =?",(id,))
    return cursor1.fetchone()
    