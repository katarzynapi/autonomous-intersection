# Autonomous Intersection

The aim of the project is simulating natural-looking traffic flow on various kinds of intersections. To achieve this goal a multiagent discrete non-deterministic model was created. It is based on the extension of the Nagel-Schreckenberg model proposed in [this](https://link.springer.com/chapter/10.1007/978-3-319-32152-3_48?fbclid=IwAR09CeDY-FHudgaqjKouczsxdzxOOMsXno-OseYgVT_sb_aD0lgBrsfvBsY) article.

## Table of contents
[Proposed model](https://github.com/katarzynapi/autonomous-intersection/blob/master/README.md#proposed-model):

  * [Road representation](https://github.com/katarzynapi/autonomous-intersection/blob/master/README.md#road-representation)

  * [Cars movement](https://github.com/katarzynapi/autonomous-intersection/blob/master/README.md#cars-movement)

  * [Updating model](https://github.com/katarzynapi/autonomous-intersection/blob/master/README.md#updating-model)

  * [Randomness in the model](https://github.com/katarzynapi/autonomous-intersection/blob/master/README.md#randomness-in-the-model)

[Implementation details](https://github.com/katarzynapi/autonomous-intersection/blob/master/README.md#implementation-details)

[Simulation examples](https://github.com/katarzynapi/autonomous-intersection/blob/master/README.md#simulation-examples):
  * [Intersection with lights](https://github.com/katarzynapi/autonomous-intersection/blob/master/README.md#intersection-with-lights)
  * [Avoiding a blockade](https://github.com/katarzynapi/autonomous-intersection/blob/master/README.md#avoiding-a-blockade)
[User guide](https://github.com/katarzynapi/autonomous-intersection/blob/master/README.md#user-guide)
  * [Downloading project](https://github.com/katarzynapi/autonomous-intersection/blob/master/README.md#downloading-project)
  * [Running examples](https://github.com/katarzynapi/autonomous-intersection/blob/master/README.md#running-examples)
  * [Map preparation](https://github.com/katarzynapi/autonomous-intersection/blob/master/README.md#map-preparation)
  * [Cars generation and paths ascribing](https://github.com/katarzynapi/autonomous-intersection/blob/master/README.md#cars-generation-and-paths-ascribing)
  * [Adding traffic lights](https://github.com/katarzynapi/autonomous-intersection/blob/master/README.md#adding-traffic-lights)
  * [Adding blockade](https://github.com/katarzynapi/autonomous-intersection/blob/master/README.md#adding-blockade)
  * [Simulation steps](https://github.com/katarzynapi/autonomous-intersection/blob/master/README.md#simulation-steps)

## Proposed Model

### Road representation
The road is divided into cells with diameter = 1 m. Each cell may have forward, backward, right and left neighbour. It also holds information about agent and obstacles (blockades, traffic lights) if present. There is always at most one agent on cell but one agent may occupy many cells depending on it's length. Cells form paths that cars can take. One cell may belong to many different paths.

### Cars movement
Possible speeds of the cars are discrete and vary from 1 cell per time unit (2 m/s) to 10 cells per time unit (20 m/s) (of course velocity = 0 m/s is also possible). Possible accelerations are -1, 0 or 1. Acceleration is used only for computing new velocity so the movement is treated as uniform motion during computing new car position or computing stopping distances.

In __step()__ method car agent perform following actions:
1. scanning for possible obstacles
2. updating route if needed
3. computing new acceleration
4. computing new velocity
5. computing new location

Description of actions:
1. Car agent obtains information about obstacles on it’s path from the cells of the path.
2. Here the behaviour of the car depends on the type of the current path. If the path type is MAIN the path will be changed only if there is a blockade on the current path and there is another path available. If the path type is OPPOSITE, which means that the car is going against the tide, it will try to get back to MAIN path. If the path type is ALTERNATIVE, which means that the car changed lane on multi-lane road, it will be changed only if car cannot obtain the border of the map without changing lane i.e. there is an obstacle on the path or path ends before some crossroads.
3. First, the distance to the nearest obstacle on the path is calculated. It may be a blockade, red traffic lights or other agent on the path. On the basis of the distance to the obstacle new acceleration is set (if the obstacle is moving distance is increased by its velocity). If the distance is 0, the car shouldn’t move. If the distance is too short to stop the car won’t try to do this (imagine a driver who spotted light changing to red but was too close and just passed it). If there is just enough space to stop the car starts slowing down by setting acceleration to -1. If the obstacle is seen in the distance the car keeps constant velocity (acceleration = 0). If the obstacle is far away or there are no obstacles at all, the car’s acceleration is set to 1 to achieve velocity of  14 m/s (50 km/h) or if the velocity is already this high it stays constant.
4. Computed acceleration is added to the current velocity to obtain new velocity. There is also a mechanism which prevents setting velocity to negative values.
5. Distance to go equals the velocity. This is because of treating movement at the moment as uniform motion.

### Updating model

Simulation is performed by calling model’s method step() in a loop. This method consists of updating lights and  calling _step()_ (see [Cars movement](https://github.com/katarzynapi/autonomous-intersection/blob/master/README.md#cars-movement)) and _advance()_ methods for all agents. More details are described [here](https://github.com/katarzynapi/autonomous-intersection/blob/master/README.md#simulation-steps).
This way of updating the model is based on the idea used in [SimultanousActivation](https://mesa.readthedocs.io/en/master/apis/time.html#mesa.time.SimultaneousActivation) scheduler from Mesa library (however, we don’t use Mesa). It requires that each agent has two methods: step and advance. step() activates the agent and stages any necessary changes, but does not apply them yet. advance() then applies the changes.

### Randomness in the model
In the model simulation the following parameters may be random:
  * car generation (time)
  * path selection for generated car
  * selection of cars colour
  * selection of cars length

## Implementation details
The project was implemented in Python 3.0. The following packages were used:
  * _cv2_ - visualization
  * _numpy_ - support for arrays management
  * _dill_ - object serialization and deserialization
  * _random_ - generating random numbers and choosing random list elements

All above-mentioned packages can be installed using command:
```sh
pip install <name_of_package>
```

## Simulation examples

### Intersection with lights
The simulation presents car movement on the crossing of two single-lane roads with lights. It is presented on the exemplary map fragment taken from OpenStreetMap.
[![N|Solid](https://raw.githubusercontent.com/katarzynapi/autonomous-intersection/master/pictures_report/map.png)](https://raw.githubusercontent.com/katarzynapi/autonomous-intersection/master/pictures_report/map.png)

Before performing simulation, the structure of roads was loaded to the model data structure as described in [Map preparation](https://github.com/katarzynapi/autonomous-intersection/blob/master/README.md#map-preparation) section. Also lights were added to proper cells on the crossing entering points. An entering-point cell can have more than one light assigned. Every light is ascribed to a path, to which it applies. 
[![N|Solid](https://raw.githubusercontent.com/katarzynapi/autonomous-intersection/master/pictures_report/lights_location.png)](https://raw.githubusercontent.com/katarzynapi/autonomous-intersection/master/pictures_report/lights_location.png)

During the simulation, cars are generated randomly at the beginnings of roads. Each car has predefined:
* destination and a path (a list of consecutive cells), which leads to this destination
* color
* length.

Cars can go straight through the crossing, turn right or turn left. 
Lights operation is based on the following sequence of paths, which have respectively green light assigned:
1. paths starting from the *top and bottom* inputs for cars going *straight* and turning *right*
2. paths starting from the *top and bottom* inputs for cars going turning *left*
3. paths starting from the *left and right* inputs for cars going *straight* and turning *right*
4. paths starting from the *left and right* inputs for cars going turning *left*

After every step of the above-mentioned sequence, all lights are changed to red for a short period (2 seconds). It is done in order to avoid collisions of cars, which enter the crossing with cars, which haven’t already left the crossing. The whole sequence is looped.

Interpretation of the lights located on the map:
[![N|Solid](https://raw.githubusercontent.com/katarzynapi/autonomous-intersection/master/pictures_report/right.png)](https://raw.githubusercontent.com/katarzynapi/autonomous-intersection/master/pictures_report/lights_interpret.png)

Exemplary states during simulation:
  * going **straight** and turning **right** (1st step in sequence)
  
[![N|Solid](https://raw.githubusercontent.com/katarzynapi/autonomous-intersection/master/pictures_report/right.png)](https://raw.githubusercontent.com/katarzynapi/autonomous-intersection/master/pictures_report/right.png)
  * turning **left** (2nd step in sequence):
  
[![N|Solid](https://raw.githubusercontent.com/katarzynapi/autonomous-intersection/master/pictures_report/left.png)](https://raw.githubusercontent.com/katarzynapi/autonomous-intersection/master/pictures_report/left.png)
  * **all lights red** (state between all sequence steps):
  
[![N|Solid](https://raw.githubusercontent.com/katarzynapi/autonomous-intersection/master/pictures_report/all_red.png)](https://raw.githubusercontent.com/katarzynapi/autonomous-intersection/master/pictures_report/all_red.png)

### Avoiding a blockade
The second simulation was performed do show blockades avoiding. It presents car movement on a double-lane road with two obstacles. There is one obstacle per one lane, what is presented on the exemplary map fragment.
[![N|Solid](https://raw.githubusercontent.com/katarzynapi/autonomous-intersection/master/pictures_report/all_red.png)](https://raw.githubusercontent.com/katarzynapi/autonomous-intersection/master/pictures_report/blockade_map.png)

According to rules described in [Cars movement](https://github.com/katarzynapi/autonomous-intersection/blob/master/README.md#cars-movement), cars are changing lanes in order to avoid blockades. Their changing currently occupied lane only if there is some obstacle on their near path fragment.

Exemplary state during simulation:
[![N|Solid](https://raw.githubusercontent.com/katarzynapi/autonomous-intersection/master/pictures_report/all_red.png)](https://raw.githubusercontent.com/katarzynapi/autonomous-intersection/master/pictures_report/blockade.png)

## User guide

### Downloading project
All project files are located on github [AutonomousIntersection](https://github.com/katarzynapi/autonomous-intersection). Clone the repository or download files directly from github page. 

### Running examples
You can open the project in an IDE or run it directly in a console. To run the simulation execute proper _main___*.py_ file. If you use a console, go to catalog with main file and execute
```sh
python main_*.py
```
List of exemplary main files:
  * main_lights.py
  * main_blocks.py

#### Map preparation
The road fragments were discretized by dividing them into adjacent cells as mentioned in Road representation section. The process of discretization was partially automatized. After manual drawing cell in the map, proper cell coordinates were automatically scanned and loaded to the model data structure.

Adding cells of one line to the model (unique circle colour is used to distinguish cells from single lane):
```python
green = [87, 193, 135] #rgb representation
for i, row in enumerate(img):
    for j, col in enumerate(row):
        if np.array_equal(green, col) or np.array_equal(nw, col) or np.array_equal(sw, col):
            print(counter)
            counter+=1
            cv2.circle(clean_img, (j, i), 3, (0, 0, 0), 2)
            cv2.imshow('image', clean_img)
            cv2.waitKey(1)
            model.grid.addCell(j, i, autointer.enums.CellType.ROAD)
```
Adding cells neighbours:
```python
#add cells' f and b neighbours
for i, cell in enumerate(model.grid.cells):
    if cell.if_border == autointer.enums.IfBorder.INPUT:
        cell.f_neighbour = model.grid.cells[i+1]
    elif cell.if_border == autointer.enums.IfBorder.NOT:
        cell.f_neighbour = model.grid.cells[i+1]
        cell.b_neighbour = model.grid.cells[i-1]
    elif cell.if_border == autointer.enums.IfBorder.OUTPUT:
        cell.b_neighbour = model.grid.cells[i-1]
#add cells' l and r neighbours
for o_cell, g_cell in zip (model.grid.cells[:int(cells_number/2)], model.grid.cells[int(cells_number/2):]):
    o_cell.l_neighbour = g_cell
    g_cell.r_neighbour = o_cell
```
Adding input and output cells to the model:
```python
for cell in model.grid.cells:
    if cell.if_border == autointer.enums.IfBorder.INPUT:
        model.grid.inputs.append(cell)
    if cell.if_border == autointer.enums.IfBorder.OUTPUT:
        model.grid.outputs.append(cell)
```
In order to save time, the whole process is not performed in every simulation execution. The model with map structure is created once and then serialized (using _dill_ library) and stored in a file (__model*.d__). The file can then be deserialized and used in every simulation execution.
Serialization and deserialization:
```python
dill.dump( model, open( "model.d", "wb" ) ) #serialization
model = dill.load( open( "model.d", "rb" ) ) #deserialization
```
### Cars generation and paths ascribing
To add a new car (agent), the following steps must be performed:
  * agent object generation: `model.generateAgent()`
  * parameters assignment: `model.agents[-1].color = color’ (color is stored as rgb in a list e.g. [255 255 255]) and ‘model.agents[-1].length = length` (length is an integer value)
  * paths ascribing: `model.agents[-1].ascribe_paths(model.paths)`
  * path selection: `model.agents[-1].place_on_grid(path_in, path_out)` (path_in and path_out are Cell objects, which are the beginning and ending of selected path)

### Adding traffic lights
To add a new light to the model, the following steps must be performed:
  * lights object generation: `model.lights.append(autointer.Lights())`
  * specifying lights location: `model.lights[-1].location = model.grid.cells[cell_idx]`
  * ascribing list of paths, to which lights are related: `model.lights[-1].connected_paths = [path1, path2, path3]`
  * initializing lights colour (green is default): `model.lights[-1].colour = enums.Colour.RED`
  * assigning lights as an obstacle on the proper cell (adding to its list of obstacles): `model.grid.cells[cell_idx].obstacles.append(model.lights[-1])`

### Adding blockade
To add a new blockade to the model, the following steps must be performed:
  * blockade object generation: `model.obstacles.append(autointer.Blockade())`
  * specifying blockade location: `model.obstacles[-1].location = model.grid.cells[cell_idx]`
  * ascribing list of paths, to which the blockade is related: `model.obstacles[-1].connected_paths = [path1, path2, path3]`
  * assigning blockade as an obstacle on the proper cell (adding to its list of obstacles): `model.grid.cells[cell_idx].obstacles.append(model.obstacles[-1])`

### Simulation steps
In every simulation step, model.step() method is executed. It consists of three main substeps:
  * lights _change()_ method (updating lights according to defined rules):
```python
for l in self.lights:
   l.change()
```
  * agent _step()_ method execution (scanning for obstacles, updating route if needed, computing new acceleration, velocity and location):
```python
for a in self.agents:
   a.step()
```
  * agent _advance()_ method execution (updating position, acceleration and velocity for all agents, based on values calculated in _step()_ method):
```python
for a in self.agents:
   a.advance()
```

## Summary



