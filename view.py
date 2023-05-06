from tkinter import *
from properites import *


class View:
    def __init__(self):
        self.win = Tk()
        self.win.configure(background="black")
        self.win.attributes("-fullscreen", True)
        self.win.title("pypong")
        self.pixel_matrix = []
        self.p1_lbl = Label(self.win, text="0", font=LBL_FONT, bg="black", fg="white", width=2)
        self.p2_lbl = Label(self.win, text="0", font=LBL_FONT, bg="black", fg="white", width=2)
        self.canvas = Canvas(self.win, height=DIMS[0]*PIXEL_SIZE, width=DIMS[1]*PIXEL_SIZE)
        for i in range(DIMS[0]):
            tmp_l = []
            for j in range(DIMS[1]):
                tmp_l.append(self.canvas.create_rectangle(PIXEL_SIZE*j, PIXEL_SIZE*i, PIXEL_SIZE*(j+1),
                                                          PIXEL_SIZE*(i+1), fill="black", outline="black"))
            self.pixel_matrix.append(tmp_l)
        
        self.p1_lbl.grid(column=0, row=1, sticky='n', pady=50)
        self.canvas.grid(column=1, row=1)
        self.p2_lbl.grid(column=2, row=1, sticky='n', pady=50)
        self.win.grid_columnconfigure(0, weight=1)
        self.win.grid_columnconfigure(2, weight=1)
        self.win.grid_rowconfigure(0, weight=1)
        self.win.grid_rowconfigure(2, weight=1)
        return
    
    def get_window(self):
        return self.win
    
    def draw_pixel(self, row: int, column: int, color: str) -> None:
        self.canvas.itemconfigure(self.pixel_matrix[row][column], fill=color, outline=color)
        
    def draw_terrain(self, objects_coords: list[tuple[int, int]]) -> None:
        for i in range(DIMS[0]):
            for j in range(DIMS[1]):
                if (i, j) in objects_coords and self.canvas.itemcget(self.pixel_matrix[i][j], "fill") == "black":
                    self.draw_pixel(i, j, "white")
                elif (i, j) not in objects_coords and self.canvas.itemcget(self.pixel_matrix[i][j], "fill") == "white":
                    self.draw_pixel(i, j, "black")
        return
    
    def refresh_points(self, p1_points: int, p2_points: int) -> None:
        self.p1_lbl["text"] = str(p1_points)
        self.p2_lbl["text"] = str(p2_points)
        return 
