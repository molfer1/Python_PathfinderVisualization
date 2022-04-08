import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont


class Menu(tk.Tk):
    def __init__(self):
        #BASE SETTINGS
        tk.Tk.__init__(self)
        self.resizable(False, False)
        self.title("Python Pathfinder")
        self.title_font = tkfont.Font(family="Roboto", size=12, weight="bold")
        pos_x = (self.winfo_screenwidth() / 2) - (self.winfo_reqwidth() / 2)
        pos_y = (self.winfo_screenheight() / 2) - (self.winfo_reqheight() / 2)
        self.geometry("+%d+%d" % (pos_x, pos_y))

        # SHARED DATA
        self.user_settings = {
            "start": False,
            "map_size": tk.StringVar(),
            "start_x": tk.IntVar(),
            "start_y": tk.IntVar(),
            "goal_x": tk.IntVar(),
            "goal_y": tk.IntVar(),
        }

        # MAIN FRAME
        main_frame = tk.Frame(self)
        main_frame.grid(column=0, row=0)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        self.bind("<Motion>", self.update_values)

        # START/GOAL INPUTS
        self.start_x = ttk.Combobox(self, state="readonly", textvariable=self.user_settings["start_x"], width=5)
        self.start_y = ttk.Combobox(self, state="readonly", textvariable=self.user_settings["start_y"], width=5)
        self.goal_x = ttk.Combobox(self, state="readonly", textvariable=self.user_settings["goal_x"], width=5)
        self.goal_y = ttk.Combobox(self, state="readonly", textvariable=self.user_settings["goal_y"], width=5)

        # SIZE SELECT
        size_label = ttk.Label(self, text="Map size: ")
        size_box = ttk.Combobox(self, state="readonly", textvariable=self.user_settings["map_size"], values=("10x10", "20x20", "30x30", "40x40"))
        size_box.current(2)
        size_label.grid(column=0, row=2, sticky=("nw"), padx=20)
        size_box.grid(column=1, row=2, columnspan=2, sticky=("nw"))

        # START POINT
        startLabel = ttk.Label(self, text="Start (x,y): ")
        startLabel.grid(column=0, row=3, sticky=("nw"), pady=5, padx=20)
        self.start_x.grid(column=1, row=3)
        self.start_y.grid(column=2, row=3)

        # GOAL POINT
        goalLabel = ttk.Label(self, text="Goal (x,y): ")
        goalLabel.grid(column=0, row=4, sticky=("nw"), pady=5, padx=20)
        self.goal_x.grid(column=1, row=4)
        self.goal_y.grid(column=2, row=4)

        # QUIT/START
        btn_quit = ttk.Button(self, text="Quit", command=lambda: self.quit())
        btn_start = ttk.Button(self, text="Start", command=lambda: self.start())
        btn_quit.grid(column=0, row=5, pady=30, padx=15)
        btn_start.grid(column=3, row=5, pady=30, padx=15)

    def quit(self):
        self.destroy()

    def start(self):
        self.user_settings['start'] = True
        self.destroy()

    def update_values(self, event):
        tab = []
        size_selection = self.user_settings["map_size"].get()
        if size_selection == "10x10":
            tab = [i for i in range(10)]
        elif size_selection == "20x20":
            tab = [i for i in range(20)]
        elif size_selection == "30x30":
            tab = [i for i in range(30)]
        elif size_selection == "40x40":
            tab = [i for i in range(40)]

        self.start_y["values"] = tab
        self.start_x["values"] = tab
        self.goal_x["values"] = tab
        self.goal_y["values"] = tab


