import sqlite3


class LeaderboardData:
    def __init__(self):
        self.database_name = "_2048_Leaderboards"
 
    def add_data(self, name, score):
        if name and score and name.strip() != "":
            try:
                conn = sqlite3.connect(f"{self.database_name}.db")
                curr = conn.cursor()
                
                curr.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.database_name} (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        score INTEGER)
                """)
                
                curr.execute(f"""
                    INSERT INTO {self.database_name}(name, score) VALUES (?, ?)""",
                (name, score))
                
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
                        name TEXT,
                        score INTEGER)
                """)
                
            curr.execute(f"""
                SELECT name, score FROM {self.database_name}
            """)
                
            values = []
            datas = curr.fetchall()
            if datas:
                for name, score in datas:
                    values.append([name, score])
                return values
                
        except sqlite3.Error as e:
            print(f"Database Error: {e}")
                
        finally:
            if curr:
                curr.close()
            if conn:
                conn.close()
        
    def delete_lower_score(self):
        try:
            conn = sqlite3.connect(f"{self.database_name}.db")
            curr = conn.cursor()
                
            curr.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.database_name} (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        score INTEGER)
                """)
            
            curr.execute(f"""
                SELECT score FROM {self.database_name}
            """)
            
            scores = curr.fetchall()
            if not scores:
                return None
                
            scores = [score[0] for score in scores]
            
            if len(scores) > 10:
                scores.sort()
                lowest_score = scores[0]
                
                curr.execute(f"""
                    DELETE FROM {self.database_name}
                    WHERE score = (?)""", (lowest_score,))
                conn.commit()
                
        except sqlite3.Error as e:
            print(f"Database Error: {e}")
                
        finally:
            if curr:
                curr.close()
            if conn:
                conn.close()
                
    def check_if_new_top(self, player_score):
        try:
            conn = sqlite3.connect(f"{self.database_name}.db")
            curr = conn.cursor()
                
            curr.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.database_name} (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        score INTEGER)
                """)
            
            curr.execute(f"""
                SELECT score FROM {self.database_name}
            """)
            
            scores = curr.fetchall()
            if not scores:
                return True
            elif len(scores) <= 10:
                return True
                
            for (score,) in scores:
                if player_score > score:
                    return True
            return False
                
        except sqlite3.Error as e:
            print(f"Database Error: {e}")
                
        finally:
            if curr:
                curr.close()
            if conn:
                conn.close()
        
    def delete(self):
        try:
            conn = sqlite3.connect(f"{self.database_name}.db")
            curr = conn.cursor()
                
            curr.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.database_name} (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
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
#    db = LeaderboardData()
#    n = ["jerald", "zygarde", "judy", "jerick", "pisot"]
#    s = [1, 2, 3, 4, 5]
#    for nm, sc in zip(n, s):
#        db.add_data(nm, sc)
#    if db.get_data():
#        for name, score in db.get_data():
#            pass
#        db.delete_lower_score()
#    else:
#        print("nothing to get")
#        
#    db.delete()
