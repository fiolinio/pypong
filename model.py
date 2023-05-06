from properites import BARS_GAP, DIMS, Direction
from random import choice


class GameObject:
    def __init__(self):
        if type(self) is GameObject:
            raise TypeError("GameObject class should not be instantiated directly")
        self.row, self.col = 0, 0
        self.dims = []
        return
    
    def get_coords(self) -> list[tuple[int, int]]:
        if not self.dims:
            raise AttributeError("The object you are trying to use has no defined dimensions.")
        return list(map(lambda c: (c[0]+self.row, c[1]+self.col), self.dims))
            

class Bar(GameObject):
    def __init__(self, axis: int):
        super().__init__()
        self.dims = [(2, 0), (1, 0), (0, 0), (-1, 0), (-2, 0)]
        self.row = DIMS[0]//2
        self.col = axis  # Constant
        return

    def valid_pos(self):
        for c in self.get_coords():
            if not c[0] in range(DIMS[0]):
                return False
        return True

    def move(self, dir: Direction):
        p_row = self.row
        match dir:
            case Direction.DOWN:
                self.row += 1
            case Direction.UP:
                self.row -= 1
            case _:
                raise ValueError("Direction must be UP or DOWN")
        if not self.valid_pos():
            self.row = p_row
        return


class Ball(GameObject):
    def __init__(self, mid_r, mid_c):
        super().__init__()
        self.mid_r, self.mid_c = mid_r, mid_c
        self.row, self.col = mid_r, mid_c
        self.dims = [(0, 0)]
        self.lr_orientation = choice([Direction.LEFT, Direction.RIGHT])
        self.du_orientation = choice([Direction.DOWN, Direction.UP])
        return
    
    def bar_collision(self, l_bar: Bar, r_bar: Bar) -> bool:
        if self.lr_orientation == Direction.LEFT:
            if (self.row, self.col-1) in l_bar.get_coords():
                return True
            if self.du_orientation == Direction.UP:
                return (self.row-1, self.col-1) in l_bar.get_coords()
            else:
                return (self.row+1, self.col-1) in l_bar.get_coords()
        else:
            if (self.row, self.col+1) in r_bar.get_coords():
                return True
            if self.du_orientation == Direction.UP:
                return (self.row-1, self.col+1) in r_bar.get_coords()
            else:
                return (self.row+1, self.col+1) in r_bar.get_coords()
    
    def side_collision(self) -> bool:
        return self.row == 0 or self.row == DIMS[0]-1
    
    def lose_collision(self) -> int:
        if self.col == 0:
            return 1
        elif self.col == DIMS[1]-1:
            return 2
        else:
            return 0
        
    def reset_ball(self):
        self.__init__(self.mid_r, self.mid_c)
        return
    
    def move(self, l_bar: Bar, r_bar: Bar) -> None:
        if self.side_collision():
            self.du_orientation = Direction.UP if self.du_orientation == Direction.DOWN else Direction.DOWN
        
        if self.bar_collision(l_bar, r_bar):
            self.lr_orientation = Direction.LEFT if self.lr_orientation == Direction.RIGHT else Direction.RIGHT
        
        if self.lr_orientation == Direction.LEFT:
            self.col -= 1
        else:
            self.col += 1
        
        if self.du_orientation == Direction.UP:
            self.row -= 1
        else:
            self.row += 1
        return
            

class Terrain:
    def __init__(self):
        self.l_bar, self.r_bar = Bar(BARS_GAP), Bar(DIMS[1]-1-BARS_GAP)
        self.ball = Ball(DIMS[0]//2, DIMS[1]//2)
        self.objects = []
        return
    
    def get_all_object_coords(self):
        objects_coords = []
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if isinstance(attr, GameObject):
                objects_coords += attr.get_coords()
        return objects_coords
    
    def move_bar(self, player: int, dir: Direction):
        match player:
            case 1:
                self.l_bar.move(dir)
            case 2:
                self.r_bar.move(dir)
            case _:
                raise ValueError("Player ID must be 1 or 2")
        return
    
    def move_ball(self):
        self.ball.move(self.l_bar, self.r_bar)
        return
    
    def ball_lose(self):
        return self.ball.lose_collision()
    
    def reset_ball(self):
        self.ball.reset_ball()
        return
        