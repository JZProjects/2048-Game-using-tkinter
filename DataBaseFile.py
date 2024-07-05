import sqlite3
from tkinter import messagebox


class DataBase:
    def __init__(self):
        self.database_name = "_2048_GameSave"
 
    def add_data(self, score, values):
        data = " : ".join(values)
        if data:
            try:
                conn = sqlite3.connect(f"{self.database_name}.db")
                
                curr = conn.cursor()
                
                curr.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.database_name} (
                        id INTEGER PRIMARY KEY,
                        numbers TEXT,
                        score INTEGER)
                """)
                
                curr.execute(f"""
                    INSERT INTO {self.database_name}(numbers, score) VALUES (?,?)""",
                (data,score))
                
                messagebox.showinfo("Success", "Game data save successfully")
        
                conn.commit()
                
            except sqlite3.Error as e:
                print(f"Database Error: {e}")
                
            finally:
                if curr:
                    curr.close()
                if conn:
                    conn.close()
        
    def get_data(self):
        try:
            conn = sqlite3.connect(f"{self.database_name}.db")
                
            curr = conn.cursor()
                
            curr.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.database_name} (
                        id INTEGER PRIMARY KEY,
                        numbers TEXT,
                        score INTEGER)
                """)
                
            curr.execute(f"""
                SELECT numbers, score FROM
                {self.database_name}
            """)
            
            datas = curr.fetchone()
            if datas:
                values = datas[0].split(" : ")
                score = datas[1]
                return score, values
                
            conn.commit()
                
        except sqlite3.Error as e:
            print(f"Database Error: {e}")
                
        finally:
            if curr:
                curr.close()
            if conn:
                conn.close()
        
    def check_game_save(self):
        try:
            conn = sqlite3.connect(f"{self.database_name}.db")
                
            curr = conn.cursor()
                
            curr.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.database_name} (
                        id INTEGER PRIMARY KEY,
                        numbers TEXT,
                        score INTEGER)
                """)
                
            curr.execute(f"""
                SELECT numbers FROM
                {self.database_name}
            """)
             
            if curr.fetchone():
                return True
            return False
            conn.commit()
                
        except sqlite3.Error as e:
            print(f"Database Error: {e}")
                
        finally:
            if curr:
                curr.close()
            if conn:
                conn.close()
                        
    def delete_save_data(self):
        try:
            conn = sqlite3.connect(f"{self.database_name}.db")
                
            curr = conn.cursor()
                
            curr.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.database_name} (
                        id INTEGER PRIMARY KEY,
                        numbers TEXT,
                        score INTEGER)
                """)
                
            curr.execute(f"""
                DELETE FROM {self.database_name}
            """)
            conn.commit()
                
        except sqlite3.Error as e:
            print(f"Database Error: {e}")
                
        finally:
            if curr:
                curr.close()
            if conn:
                conn.close()
        
#if __name__ == "__main__":
#    db = DataBase()
#    db.delete_save_data()
#    s = 10
#    l = ["1","2","3","4","5"]
#    #print(l)
#    db.add_data(s, l)
#    if db.check_game_save():
#        sc, n = db.get_data()
#        print("Fin",sc, n)
#        print("done")