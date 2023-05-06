from properites import Direction
from model import *
from view import *
from threading import Thread


class Controller:
    def __init__(self, view: View, terrain: Terrain):
        self.view = view
        self.terrain = terrain
        self.win = self.view.get_window()
        self.p1_points = 0
        self.p2_points = 0
        
        self.win.bind("<Key>", self.keypress)
        
        Thread(target=self.move_ball_loop).start()
        self.play()
        self.win.mainloop()
        pass
    
    def keypress(self, event):
        match event.keycode:
            case 38:
                t = Thread(target=self.move_rbar_up)
            case 40:
                t = Thread(target=self.move_rbar_down)
            case 90:
                t = Thread(target=self.move_lbar_up)
            case 83:
                t = Thread(target=self.move_lbar_down)
            case 27:
                self.win.destroy()
                return 
            case _:
                return
        t.start()
        return
    
    def play(self):
        self.view.draw_terrain(self.terrain.get_all_object_coords())
        self.view.refresh_points(self.p1_points, self.p2_points)
        self.win.after(REFRESH_RATE, self.play)
    
    def move_ball_loop(self):
        lose = self.terrain.ball_lose()
        if lose != 0:
            match lose:
                case 1:
                    self.p2_points += 1
                case 2:
                    self.p1_points += 1
            self.terrain.reset_ball()
            self.win.after(NEW_BALL_DELAY, self.move_ball_loop)
            return
        self.terrain.move_ball()
        self.win.after(BALL_DELAY, self.move_ball_loop)
        return
    
    def move_lbar_up(self):
        self.terrain.move_bar(1, Direction.UP)
        return
    
    def move_lbar_down(self):
        self.terrain.move_bar(1, Direction.DOWN)
        return
    
    def move_rbar_up(self):
        self.terrain.move_bar(2, Direction.UP)
        return
    
    def move_rbar_down(self):
        self.terrain.move_bar(2, Direction.DOWN)
        return
