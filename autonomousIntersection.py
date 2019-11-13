import math
from enum import Enum

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

#_________________________________________________________________________
# map

class Cell:
    def __init__(self, x_coords=0.0, y_coords=0.0, surface_type=CellType.NULL):
        self.coords = Coordinates(x_coords, y_coords)
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

class Grid:
    def __init__(self, min_x_coords, min_y_coords, max_x_coords, max_y_coords):
        self.coords_range = min_x_coords, min_y_coords, max_x_coords, max_y_coords
        self.cells = []
    def addCell(self, x_coords, y_coords, cell_type):
        self.cells.append(Cell(x_coords, y_coords, cell_type))
    def getCells(self):
        return self.cells
    def getCoordsRange(self):
        return self.coords_range
		
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
        return math.sqrt((coords.x - self.x)^2 + (coords.y - self.y)^2)

class Obstacle:
    def __init__():
        self.location = None            # typ to Cell (nie Coordinates)
        self.visibility = 0.0
        self.agent_types = []
        self.speed_limit = 0.0
        
class Lights(Obstacle):
    def __init__():
        super.__init__()
        self.colour = Colour.GREEN
        
class Blockade(Obstacle):
    #przeszkoda, którą trzeba wyminąć
    def __init__():
        super.__init__()

class Crossing_Entering(Obstacle):
    def __init__():
        super.__init__()
        self.for_which_road = []
        self.cells_to_check = []

#_________________________________________________________________________
# agents

class GeneralAgent:
    _counter = -1
    def __init__(self):
        GeneralAgent._counter += 1
        self.id = GeneralAgent._counter
        self.location = []              # lista Cell; 1szy el. - head
        self.head = 0.0
        self.tail = 0.0
        self.velocity = 0.0
        self.max_velocity = 0.0
        self.acceleration = 0.0
        self.max_acceleration = 0.0
        self.max_deceleration = 0.0
        self.length = 0.0
        self.visibility = 0.0           # z jakiej odległości widać agenta
        self.field_of_view = 0.0        # na jaką odległość widzi agent
        self.destination = None
        self.path = []
        self.obstacles = []
        self.agent_on_path = None       # najbliższe auto przed
        self.new_position_of_head = None
        self.new_velocity = 0.0
        self.new_acceleration = 0.0

    def how_many_cells():
        return round(self.length)

    def reached_destination():
        #jeśli przód agenta jest blisko celu, to cel uznajemy za osiągnięty
        if self.location[0].coords.calculate_distance(self.destination) > self.length:
            return false
        else:
            return true

    def find_path():
        #TODO
        # tutaj jakiś ambitny algorytm wyznaczający trasę w oparciu o lokalizację i cel
        print ("to jest tylko po to, żeby nie leciał błąd wcięcia")        

    def visible_path():
        # powinno zwracać ten fragment wyznaczonej trasy, który agent widzi
        return [c for c in self.path if self.location[0].coords.calculate_distance(c.coords) > self.field_of_view]

    def scan_for_obstacles():
        current_obstacles = []
        for c in visible_path():
            current_obstacles += c.obstacles
        self.obstacles = current_obstacles

    def find_first_agent_on_path():
        return next((x.agent for x in visible_path() if x.agent is not None), None)

    # na razie radosna wersja zakładająca, że na drodze są tylko inne auta i jedyna opcja to zwolnić
    # nie ogarniam tych wzorów z artykułu :(
    def compute_new_velocity():
        #TODO
        print ("to jest tylko po to, żeby nie leciał błąd wcięcia")

    def compute_new_acceleration():
        #TODO
        print ("to jest tylko po to, żeby nie leciał błąd wcięcia")

    def compute_new_location():
        #TODO
        print ("to jest tylko po to, żeby nie leciał błąd wcięcia")

    #aby wszyscy ruszali się jednocześnie, najpierw trzeba policzyć nowe parametry, a jak wszystkie będą policzone, to je przypisać. Dlatego dwie metody (wzorowałam się na SimultaneousActivation z mesa)

    def step(self):
        self.scan_for_obstacles()
        if any(isinstance(x, Blockade) for x in self.obstacles):
            self.find_path()
        self.compute_new_velocity()
        self.compute_new_acceleration()
        self.compute_new_location()

    def advance(self):
        #TODO
        # gdzieś tu trzeba jeszcze wywalić z path te komórki, które zostały za samochodem
        print ("to jest tylko po to, żeby nie leciał błąd wcięcia")
        
#_________________________________________________________________________
# model

class IntersectionModel:

    def __init__(self, min_coords, max_coords):
        self.steps = 0
        self.time = 0
        self.agents = []
        self.grid = Grid(min_coords, max_coords)    # współrzędne lewego dolnego i prawego górnego rogu; wyznaczają wielkość mapy

    def generate_agents():
        #TODO
        pass
        print ("to jest tylko po to, żeby nie leciał błąd wcięcia") # można użyć słowa pass :)

    def remove_agents():
        for a in self.agents:
            if a.reached_destination():
                self.agents.remove(a)

    def step(self):
        for a in self.agents:
            a.step()
        for a in self.agents:
            a.advance()
        self.steps += 1
        self.time += 0.5                    # bo za artykułem Wąsa robimy update co pół sekundy