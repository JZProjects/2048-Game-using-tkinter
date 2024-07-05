from tkinter import *
from tkinter import messagebox, simpledialog
from tkinter import ttk
from random import choice, randint
from DataBaseFile import DataBase
from GameLeaderboardFile import LeaderboardData


class Game2048GUI:
    def __init__(self, master):
        self.master = master
        
        self.width = master.winfo_screenwidth()//1.1
        self.height = master.winfo_screenheight()//1.1
        self.master.config(bg="black")
        self.master.title("2048GameClassic")
        self.display_game_screen()
        self.display_control_buttons()
        self.new_game()
    
    def display_game_screen(self):
        
        self.score = 0
        self.blocks = []
        self.count_track = 0
        self.db = DataBase()
        self.leaderboard_file = LeaderboardData()
        
        top_frame = Frame(self.master, bg="black")
        top_frame.pack()
        
        exit_button = Button(top_frame, text="Exit", bg="tomato", fg="snow",  width=5, bd=5, font="arial 8", relief=RAISED, command=self.exit_program)
        exit_button.grid(row=0, column=2)
        
        leader_board = Button(top_frame, bg="#00B000", fg="snow", text="Leaderboards", font="Helvetica 6", width=6, bd=5, relief=RAISED, command=self.display_leaderboards)
        leader_board.grid(row=1, column=2, ipady=7, ipadx=5)
        
        recent_game_btn = Button(top_frame, text ="Recent", bg="#FF8C00", fg="snow", relief=RAISED, width=4, bd=5, command=self.continue_recent_game)
        recent_game_btn.grid(row=0, column=0, pady=(10,0))
        
        save_button = Button(top_frame, text="Save", bg="#00BFFF", fg="snow", width=4, bd=5, relief=RAISED, command=self.display_save_window)
        save_button.grid(row=1, column=0)
        
        self.score_label = Label(top_frame, text=f"Score:\n{self.score}", font=("Helvetica", 15, "bold"), bg="black", fg="snow")
        self.score_label.grid(row=0, column=1, padx=110, rowspan=2)

        self.game_frame = Frame(self.master, width=self.width, height=self.height//1.3, bd=5, relief=RAISED)
        self.game_frame.pack(pady=(40,20))
        
        id_counter = 0
        for row in range(4):
            for column in range(4):
                block = Button(self.game_frame, 
                    text="    ",
                    width=6, height=5, bd=0,
                    font=("time", 7, "bold"))
                block.grid(row=row, column=column)
                self.blocks.append(block)
                id_counter += 1
        
    def display_control_buttons(self):
        width = self.width 
        height = self.height 
        
        button_frame = Frame(self.master, bg="black")
        button_frame.pack(pady=20)
        
        right_button = Button(
            button_frame, text="→",
            font="time 10 bold",
            command=self.move_right, 
            relief=RAISED, bd=8, 
            width=int(width//100), 
            height=int(height//500))
        right_button.pack(side=RIGHT, pady=(20, 0))
        
        left_button = Button(
            button_frame, text="←", 
            font="time 10 bold",
            command=self.move_left, 
            relief=RAISED, bd=8,
            width=int(width//100), 
            height=int(height//500))
        left_button.pack(side=LEFT, pady=(20, 0))
        
        up_button = Button(
            button_frame, text="↑", 
            font="time 10 bold",
            command=self.move_up, 
            relief=RAISED, bd=8, 
            width=int(width//100), 
            height=int(height//500))
        up_button.pack(side=TOP, pady=(0,135))
        
        down_button = Button(
            button_frame, text="↓", 
            font="time 10 bold",
            command=self.move_down, 
            relief=RAISED, bd=8, 
            width=int(width//100), 
            height=int(height//500))
        down_button.pack(anchor="s")

    def add_more_blocks(self):
        count = 0
        emergency_count = 0
        indexes = []
        number_of_blocks = 2
        while count < number_of_blocks:
            index = randint(0,15)
            if self.blocks[index]["text"] == "    ":
                random_choice = choice(["2", "2", "2", "2", "2", "2", "2", "2", "2","4"])
                self.blocks[index].config(text=random_choice, bg=self.color_block(random_choice))
                self.blocks[index].config(bd=1)
                count += 1
                
            if index not in indexes:
                indexes.append(index)
                emergency_count += 1
           
            if emergency_count == 16:
                break
                
        if self.is_game_finish():
            messagebox.showinfo("Congratulations", "You win!!!")
            self.is_new_top_score()
            self.new_game(False)
        elif self.is_game_over():
            messagebox.showwarning("Mission Failed", "You lose!!!!!!")
            self.is_new_top_score()
            self.new_game(False)
            
    def is_same_block(self, next_block, prev_block):
        return self.blocks[next_block]["text"] == self.blocks[prev_block]["text"]
    
    def is_free_way(self, next_block, prev_block):
        if self.blocks[next_block]["text"] == "    ":
            return True
        elif self.blocks[next_block]["text"] != self.blocks[prev_block]["text"] and self.count_track != 0:
            return False
            
        return False
        
    def combine_block(self, next_block, prev_block):
        number = self.blocks[next_block]["text"]
        if number.isdigit():
            number_product = int(number) * 2
            self.move(next_block, prev_block, str(number_product))
            
            self.score += number_product
            self.score_label.config(text=f"Score:\n{self.score}")
            self.is_game_finish()
    
    def move_left(self):
        for i in range(len(self.blocks)):
            current_block = i
            next_block = i - 1
            restricted_block_id_left = (3, 7, 11)
            while next_block >= 0 and next_block not in restricted_block_id_left and self.is_free_way(next_block, current_block):
                self.move(next_block, current_block)
                current_block = next_block
                next_block -= 1
                   
            if next_block >= 0 and next_block not in restricted_block_id_left and self.is_same_block(next_block, current_block):
                self.combine_block(next_block, current_block)
                    
            self.count_track = 0
        self.add_more_blocks()
                    
    def move_right(self):
        for i in range(len(self.blocks), -1, -1):
            current_block = i
            next_block = i + 1
            restricted_block_id_right = (4, 8, 12)
            while next_block < 16 and next_block not in restricted_block_id_right and self.is_free_way(next_block, current_block):
                self.move(next_block, current_block)
                current_block = next_block
                next_block += 1
                            
            if next_block < 16 and next_block not in restricted_block_id_right and self.is_same_block(next_block, current_block):
                self.combine_block(next_block, current_block)
                    
            self.count_track = 0
        self.add_more_blocks()
        
    def move_up(self):
        for i in range(len(self.blocks)):
            current_block = i
            next_block = i - 4
            while next_block >= 0 and self.is_free_way(next_block, current_block):
                self.move(next_block, current_block)
                current_block = next_block
                next_block -= 4
            if next_block > -1 and self.is_same_block(next_block, current_block):
                self.combine_block(next_block, current_block)
                        
            self.count_track = 0
        self.add_more_blocks()
                    
    def move_down(self):
        for i in range(len(self.blocks), -1, -1):
            current_block = i
            next_block = i + 4
            while next_block <= 15 and self.is_free_way(next_block, current_block):
                self.move(next_block, current_block)
                current_block = next_block
                next_block += 4

            if next_block < 16 and self.is_same_block(next_block, current_block):
                self.combine_block(next_block, current_block)
                        
            self.count_track = 0
        self.add_more_blocks()
        
    def move(self, next_block, prev_block, text=None):
        if not text:
            text = self.blocks[prev_block]["text"]
           
        self.count_track += 1
        
        if text != "    ":
            self.blocks[next_block].config(text=text, bg=self.color_block(text), bd=1)
            self.blocks[prev_block].config(text="    ", bg="gainsboro", bd=0)
        
         
    def is_game_over(self):
        for i, block in enumerate(self.blocks):
            block_text = block["text"]
            if block_text == "    ":
                return False
                
            up = -4 + i
            down = 4 + i
            left = -1 + i
            right = 1 + i
            
            restricted_block_id_right = (4, 8, 12)
            restricted_block_id_left = (3, 7, 11)
            
            if (right < 16 and right not in restricted_block_id_right) and self.blocks[right]["text"] == block_text:
                return False
            elif (left >= 0 and left not in restricted_block_id_left) and self.blocks[left]["text"] == block_text:
                return False
            elif up >= 0 and self.blocks[up]["text"] == block_text:
                return False
            elif down < 16 and self.blocks[down]["text"] == block_text:
                return False
                
        return True
    
    def is_game_finish(self):
        for block in self.blocks:
            if block["text"] == "2048":
                return True
        return False
        
    def clear_game(self):
        for block in self.blocks:
            block.config(text="    ", bd=0, bg="gainsboro")
    
    def new_game(self, firstgame=True):
        if not firstgame:
            if messagebox.askyesno("Hey!!!", "You want to\nplay again!?"):
                self.score = 0
                self.score_label.config(text=f"Score:\n{self.score}")                
                self.clear_game()
                self.add_more_blocks()
            else:
                self.exit_program(True)
        else:
            self.add_more_blocks()

    def color_block(self, text):
        color_set = {
            "2": "#FFFACD", 
            "4": "#AFEEEE",
            "8": "#FFD700",
            "16": "#1E90FF",
            "32": "#9400D3",
            "64": "#FF4500",
            "128": "olive drab",
            "256": "#5F96A0",
            "512": "#C71585",
            "1024": "#0000CD",
            "2048": "#00FF7E"
        }
        
        return color_set[text]
        
    def display_leaderboards(self):
        leaderboard_frame = Toplevel(self.master)
        leaderboard_frame.resizable(False, False)
        leaderboard_frame.title("Leaderboard")
    
        leaderboards = self.leaderboard_file.get_data()

        if not leaderboards:
            messagebox.showinfo("Hey Player!!!", "There are still no current\nplayer set his record\nin our leaderboards\nPlay now to become\nthe first player to be listed!!!")
            return
        
        descending_order_board = []
        
        for name, score in leaderboards:
            descending_order_board.append([score, name])
        descending_order_board.sort(reverse=True)
    
        columns = ["rank", "name", "score"]
        table = ttk.Treeview(leaderboard_frame, show='headings', columns=columns, height=10)
        
        style = ttk.Style()
        # Set row height to 40 pixels
        style.configure("Treeview", rowheight=40)  
        
        table.pack(side=LEFT, padx=5, pady=5)
        
        table.heading('rank', text='Rank')
        table.heading('name', text='Name')
        table.heading('score', text='Score')
        
        table.column("rank", width=100, anchor='center')
        table.column("name", width=400, anchor='center')
        table.column("score", width=200, anchor='center')
        
        for index, (score, name) in enumerate(descending_order_board):
            table.insert('', END, values=(index+1, name, score))
    
        scrollbar = ttk.Scrollbar(leaderboard_frame, orient="vertical", command=table.yview)
        scrollbar.pack(side=RIGHT, fill='y')
        table.configure(yscrollcommand=scrollbar.set)
    
    def is_new_top_score(self):
        if self.leaderboard_file.check_if_new_top(self.score):
            self.register_new_top_score()
        
    def register_new_top_score(self):
        score = self.score
        name = ""
        while True:
            name = simpledialog.askstring("Hey you are one of the top scorer!!!", "What is you name?")
            if not name:
                return
            elif name.strip() == "":
                messagebox.showerror("Naming Error", "Invalid Name!!!\nPlease provide a valid name.")
                continue
            elif len(name) > 26:
                messagebox.showerror("Naming Error", "Name length excess!!!\nPlease provide a name\nwith characters below 27\ncharacters.")
                continue
            break
            
        if name:
            self.leaderboard_file.add_data(name, score)
            self.leaderboard_file.delete_lower_score()
    
    def display_save_window(self):
        if messagebox.askyesno("Hey Player!!!", "Do you want to save\nthe game data and \noverwrite the older one?"):
            self.save_game()
            
    def save_game(self):
        values = []
        for block in self.blocks:
            values.append(block["text"])
        if len(values) == 16:
            self.db.delete_save_data()
            self.db.add_data(self.score, values)
            
    def continue_recent_game(self):
        if not messagebox.askyesno("Hey Player!!!", "Are you sure you want\nplay your recent save game?"):
            return
        self.clear_game()
        if self.db.check_game_save():
            score, values = self.db.get_data()
            for value, block in zip(values, self.blocks):
                block["text"] = value
                if value != "    ":
                    block.config(bd=1, bg=self.color_block(value))
            self.score = score
            self.score_label.config(text=f"Score:\n{self.score}")
            
    def exit_program(self, is_direct_exit=False):
        if is_direct_exit or messagebox.askyesno("Hey Player!!!", "Are you sure you want\nto exit the game?"):
            self.master.destroy()
            


if __name__ == "__main__":
    root = Tk()
    Game2048GUI(root)
    root.mainloop()