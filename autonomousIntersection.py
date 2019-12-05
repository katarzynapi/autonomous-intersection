import math
from enum import Enum
import mapDrawing as mapdraw
import numpy as np
import random

class CellType(Enum):
    NULL = 0
    PAVEMENT = 1
    GRASS = 2
    BUILDING = 3
    ROAD = 4
    TRACKS = 5
    BIKE_LANE = 6
    
class Colour(Enum):
    RED = 1
    GREEN = 2

class IfBorder(Enum):
    NOT = 0
    INPUT = 1
    OUTPUT = 2

class PathType(Enum):
    MAIN = 1
    ALTERNATIVE = 2
    OPPOSITE = 3

#_________________________________________________________________________
# map

class Cell:
    def __init__(self, x_coords=0.0, y_coords=0.0, surface_type=CellType.NULL, if_border = IfBorder.NOT):
        self.coords = Coordinates(x_coords, y_coords)
        self.if_border = IfBorder.NOT
        self.surface_type = surface_type
        self.f_neighbour = None           # forward
        self.b_neighbour = None           # backward
        self.r_neighbour = None           # right
        self.l_neighbour = None           # left
        self.fr_neighbour = None
        self.fl_neighbour = None
        self.br_neighbour = None
        self.bl_neighbour = None
        self.agent = None                 # założyłam, że będzie jeden agent na jednym polu
        self.obstacles = []
    
    def getCoords(self):
        return self.coords.getCoordinates()
    
    def add_obstacle(obstacle):
        self.obstacles.append(obstacle)

    def find_fwd_and_bwd_path(self):
        fwd_path = []
        bwd_path = []
        curr_cell = self
        while curr_cell.f_neighbour is not None:
            fwd_path.append(curr_cell.f_neighbour)
            curr_cell = curr_cell.f_neighbour
        curr_cell = self
        bwd_path.append(curr_cell)
        while curr_cell.b_neighbour is not None:
            bwd_path.append(curr_cell.b_neighbour)
            curr_cell = curr_cell.b_neighbour
        return (fwd_path, bwd_path)

class Grid:
    def __init__(self, min_x_coords, min_y_coords, max_x_coords, max_y_coords):
        self.coords_range = min_x_coords, min_y_coords, max_x_coords, max_y_coords
        self.cells = []
        self.inputs = []
        self.outputs = []
    
    def addCell(self, x_coords, y_coords, cell_type):
        self.cells.append(Cell(x_coords, y_coords, cell_type))
    
    def getCells(self):
        return self.cells
    
    def getCoordsRange(self):
        return self.coords_range

class Path:
    def __init__(self, path_type, cell_list):
        self.type = path_type
        self.cells = cell_list
        
		
class Coordinates:
    def __init__(self, x_coords=0.0, y_coords=0.0):
        self.x = x_coords
        self.y = y_coords
    
    def setCoordinates(self):
        self.x = x_coords
        self.y = y_coords
    
    def getCoordinates(self):
        return self.x, self.y
    
    def calculate_distance(self, coords):
        return math.sqrt((coords.x - self.x)**2 + (coords.y - self.y)**2)

class Obstacle:
    def __init__(self):
        self.location = None            # typ to Cell (nie Coordinates)
        self.visibility = 0.0
        self.agent_types = []
        self.speed_limit = 0.0
        
class Lights(Obstacle):
    def __init__(self):
        super(Obstacle).__init__()
        self.colour = Colour.GREEN

    def change(self):
        self.colour = Colour.GREEN if self.colour == Colour.RED else Colour.RED
        
class Blockade(Obstacle):
    #przeszkoda, którą trzeba wyminąć
    def __init__(self):
        super.__init__()

class Crossing_Entering(Obstacle):
    def __init__(self):
        super.__init__()
        self.for_which_road = []
        self.cells_to_check = []

#_________________________________________________________________________
# agents


class GeneralAgent:
    _counter = -1
    far_away = 10000
    vel_table = np.array([np.arange(1,11,1),np.arange(2,22,2),np.arange(7.2,79.2,7.2)])
    def __init__(self):
        GeneralAgent._counter += 1
        self.id = GeneralAgent._counter
        self.location = []              # lista Cell; 1szy el. - head
        self.velocity = self.vel_table[0,random.randint(2,7)]        # w polach drogi na jednostkę czasu
        self.max_velocity = self.vel_table[0,9]
        self.acceleration = 0.0
        self.max_acceleration = 2       # zakładam, że auto może przyspieszać 4 m/s^2
        self.max_deceleration = -2
        self.length = 5.0
        self.visibility = 0.0           # z jakiej odległości widać agenta
        self.field_of_view = 80.0        # na jaką odległość widzi agent
        self.destination = None
        self.all_paths = []
        self.path = None                  # pierwsza komórka w path to któryś z przednich sąsiadów head
        self.obstacles = []
        self.how_many_cells_forward = 0
        self.new_velocity = 0.0
        self.new_acceleration = 0.0

    def place_on_grid(self, tail_position):
        self.location.insert(0,tail_position)
        tail_position.agent = self
        cell_to_add = tail_position
        for i in range(self.how_many_cells()-1):
            cell_to_add = cell_to_add.f_neighbour
            cell_to_add.agent = self
            self.location.insert(0,cell_to_add)

    def ascribe_paths(self, paths_list):
        self.all_paths = paths_list
        self.path = next((p for p in paths_list if p.type == PathType.MAIN), None)

    @property
    def head(self):
        if not self.location:
            return None
        return self.location[0]

    @head.setter
    def head(self, cell):
        self.location.insert(0,Cell)

    @property
    def tail(self):
        if not self.location:
            return None
        return self.location[-1]

    @tail.setter
    def tail(self, cell):
        self.location.append(cell)

    def how_many_cells(self):
        return round(self.length)

    def stopping_dist(self, dec):
        # -abs(dec) jest po to, żeby opóźnienie można było podawać z minusem lub bez
        return sum(list(range(int(self.velocity), 0, int(-abs(dec)))))

    def reached_destination(self):
        #jeśli przód agenta jest blisko celu, to cel uznajemy za osiągnięty
        if self.location[0].coords.calculate_distance(self.destination.coords) < self.length:
            #if self.head.f_neighbour == None:
            return True
        else:
            return False

    def alternative_route_exists(self):
        for p in self.all_paths:
            if (p.type == PathType.ALTERNATIVE and (self.head.r_neighbour in p.cells or self.head.r_neighbour in p.cells)):
                return True
        return False

    def opposite_route_exists(self):
        for p in self.all_paths:
            if p.type == PathType.OPPOSITE and (self.head.r_neighbour in p.cells or self.head.r_neighbour in p.cells):
                return True
        return False

    def can_safely_change_to_other_path(self, other_path_fwd, other_path_bwd):
        #gdyby się okazało, że to wszystko wali błędami, to przerobimy na zwykłą pętlę for
        (prev_dist, prev_vehicle) = next(((len(other_path_bwd)-1-i, x.agent) for i, x in other_path_bwd[::-1] if x.agent is not None), (None, None))
        (next_dist, next_vehicle) = next(((i+1, x.agent) for i, x in other_path_fwd if x.agent is not None), (None, None))
        if prev_vehicle is None:
            prev_safe = True
        else:
            prev_safe = (prev_vehicle.stopping_dist(-2) + prev_dist - self.how_many_cells() > self.stopping_dist(-2))
        if next_vehicle is None:
            next_safe = True
        else:
            next_safe = (self.stopping_dist(-2) + next_distance > next_vehicle.stopping_dist(-2))
        return (next_safe and prev_safe)

    def visible_path(self):
        # powinno zwracać ten fragment wyznaczonej trasy, który agent widzi
        return self.path.cells
        #return [c for c in self.path if self.location[0].coords.calculate_distance(c.coords) > self.field_of_view]

    def scan_for_obstacles(self):
        current_obstacles = []
        for c in self.visible_path():
            current_obstacles += c.obstacles
        self.obstacles = current_obstacles

    def calc_path_distance(self, obstacle):
        for i, c in enumerate(self.visible_path()):
            if obstacle in c.obstacles or obstacle == c.agent:
                return i+1
        return 0

    def find_first_agent_on_path(self):
        return next((x.agent for x in self.visible_path() if x.agent is not None), None)

    def find_nearest_lights(self):
        return next((obs for obs in self.obstacles if isinstance(obj, Lights)), None)

    def find_nearest_blockade(self):
        return next((obs for obs in self.obstacles if isinstance(obj, Blockade)), None)


    def update_route(self):
        if self.path.type == PathType.OPPOSITE:
            neighbour_main = self.head.neighbour_r
            main_path = next((p for p in self.all_paths if p.type == PathType.MAIN), None)
            start = main_path.index(neighbour_main)
            main_fwd = main_path[start+1:]
            main_bwd = main_path[:start+1]
            if can_safely_change_to_other_path(main_fwd, main_bwd):
                self.path.type = PathType.MAIN
                self.path.cells = main_bwd
        else:
            if self.path.type == PathType.ALTERNATIVE and self.path.cells[-1].if_border == IfBorder.NOT and len(self.path.cells) < self.stopping_dist(-1) + 10:
                neighbour_main = self.head.neighbour_r
                main_path = next((p for p in self.all_paths if p.type == PathType.MAIN), None)
                start = main_path.index(neighbour_main)
                main_fwd = main_path[start+1:]
                main_bwd = main_path[:start+1]
                if can_safely_change_to_other_path(main_fwd, main_bwd):
                    self.path.type = PathType.MAIN
                    self.path.cells = main_bwd
            else:
                blockade = self.find_nearest_blockade()
                if blockade is not None:
                    if self.path.type == PathType.ALTERNATIVE:
                        neighbour_main = self.head.neighbour_r if self.head.neighbour_r is not None else self.head.neighbour_l
                        main_path = next((p for p in self.all_paths if p.type == PathType.MAIN), None)
                        start = main_path.index(neighbour_main)
                        main_fwd = main_path[start+1:]
                        main_bwd = main_path[:start+1]
                        if can_safely_change_to_other_path(main_fwd, main_bwd):
                            self.path.type = PathType.MAIN
                            self.path.cells = main_bwd
                    else:
                        avail_alt = [p for p in self.all_paths if p.type == PathType.ALTERNATIVE and (self.head.neighbour_r in p.cells or self.head.neighbour_l in p.cells)]
                        for p in avail_path:
                            neighbour_alt = self.head.neighbour_r if self.head.neighbour_r in p else self.head.neighbour_l
                            start = p.index(neighbour_alt)
                            alt_fwd = p[start+1:]
                            alt_bwd = p[:start+1]
                            if can_safely_change_to_other_path(alt_fwd, alt_bwd):
                                self.path.type = PathType.ALTERNATIVE
                                self.path.cells = alt_fwd
        self.scan_for_obstacles()


    def compute_new_location(self):
        self.how_many_cells_forward = int(round(self.velocity))

    def compute_new_velocity(self):
        if (self.acceleration >= 0):
            self.new_velocity = min(self.velocity + self.acceleration, self.max_velocity)
        else:
            self.new_velocity = max(self.velocity + self.acceleration, 0)

    #gdzieś w tej funkcji radośnie przesądzam i trochę hardcoduję, że opóźnienie może być tylko -1 lub -2
    def compute_new_acceleration(self):
        agent_on_path = self.find_first_agent_on_path()
        lights = self.find_nearest_lights()
        blockade = self.find_nearest_blockade()
        
        l_dist = self.far_away           #jakaś losowa duża liczba - oznacza, że świateł/agenta nie ma (w założeniu nic nie jest tak daleko)
        a_dist = self.far_away
        b_dist = self.far_away
        
        if lights is not None and lights.colour == Colour.RED:
            l_dist = self.calc_path_distance(lights)
        if agent_on_path is not None:
            a_dist = self.calc_path_distance(agent_on_path) + agent_on_path.stopping_dist(-2)
        if blockade is not None:
            b_dist = self.calc_path_distance(blockade)
        dist = min(a_dist, l_dist, b_dist)
        if dist > self.stopping_dist(-1)*2:
            self.acceleration = 1 if self.velocity < 7 else 0
        #elif dist > stopping_dist(-1)*1.5:
            #self.acceleration = self.acceleration = max(self.acceleration, 0)
        elif dist > self.stopping_dist(-1):
            self.acceleration = 0
        elif dist > self.stopping_dist(-2)+2:
            self.acceleration = -1
        elif dist >= self.stopping_dist(-2)-1:
            self.acceleration = -2
        else:
            self.acceleration = max(self.acceleration, 0)

    def update_position(self):
        # powinno działać. testy by nie zaszkodziły
        # auto wjeżdża na tyle komórek path, ile wyznaczono na podstawie prędkości
        vel_len_diff = self.how_many_cells_forward - self.length
        start = vel_len_diff if vel_len_diff >= 0 else 0
        new_car_part = self.path.cells[int(start):int(self.how_many_cells_forward)]
        new_car_part.reverse()
        # dodajemy agenta dla nowych komórek
        for cell in new_car_part:
            cell.agent = self
        # auto pozostaje na swoich komórkach - tyle, o ile się przesuwa
        old_car_part = self.location[:-self.how_many_cells_forward]
        # zdejmujemy agenta z komórek, z których zjechał
        for cell in self.location[-self.how_many_cells_forward:]:
            cell.agent = None
        # nowe położenie
        self.location = new_car_part + old_car_part
        # ucinamy z path to, na co wjechało auto
        self.path.cells = self.path.cells[self.how_many_cells_forward:]


    #aby wszyscy ruszali się jednocześnie, najpierw trzeba policzyć nowe parametry, a jak wszystkie będą policzone, to je przypisać. Dlatego dwie metody (wzorowałam się na SimultaneousActivation z mesa)

    def step(self):
        pass
        self.scan_for_obstacles()
        self.update_route()
        self.compute_new_location()
        self.compute_new_velocity()
        self.compute_new_acceleration()

    def advance(self):
        self.update_position()
        self.velocity = self.new_velocity
        self.acceleration = self.new_acceleration
        
#_________________________________________________________________________
# model

class IntersectionModel:
    def __init__(self, min_x_coords, min_y_coords, max_x_coords, max_y_coords):
        self.image = None
        self.steps = 0
        self.time = 0
        self.agents = []
        self.paths = {}
        self.grid = Grid(min_x_coords, min_y_coords, max_x_coords, max_y_coords)    # współrzędne lewego dolnego i prawego górnego rogu; wyznaczają wielkość mapy
    # show agent movement
        self.lights = []
    def showAgentMovement(self, id, width):
        start_points = [a.head.getCoords() for a in self.agents]
        end_points = [a.tail.getCoords() for a in self.agents]
        mapdraw.drawNewLine(start_points, end_points, width, self.image)
    #add new agent with default parameters (can be expanded with additional parameters)
    def generateAgent(self):
        self.agents.append(GeneralAgent())

    def remove_agents(self):
        for a in self.agents:
            if a.reached_destination():
                self.agents.remove(a)

    def step(self):
        if self.time % 20 == 0:
            for l in self.lights:
                l.change()
        for a in self.agents:
            a.step()
        for a in self.agents:
            a.advance()
        self.steps += 1
        self.time += 0.5                    # bo za artykułem robimy update co pół sekundy
