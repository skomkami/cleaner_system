from simulation.simulation_loop import Simulation
from drawer.simulation_drawer import SimulationDrawer
from model.jsonHelper import fromFile
import os
import sys

cwd = os.getcwd()
if len(sys.argv) > 1:
    config_file_name = sys.argv[1]
    config_path = os.path.join(cwd, config_file_name)
else:
    config_file_name = "floor0.json"
    config_path = os.path.join(cwd, "maps", config_file_name)
floor_map = fromFile(config_path)

if len(sys.argv) > 2:
    print('drawing from source')
    simulation = SimulationDrawer(floor_map)
    simulation.draw_from_file('output/output.json')
else:
    print('running simulation')
    simulation = Simulation(floor_map)
    simulation.run_simulation()
