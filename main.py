from simulation.simulation_loop import Simulation
from drawer.simulation_drawer import SimulationDrawer
from model.jsonHelper import fromFile
import os
import sys


if len(sys.argv) < 2:
    print('specify map path')
    sys.exit(0)
config_file_name = sys.argv[1]
if config_file_name in ['--default']:
    config_file_name = "maps/floor0.json"
try:
    cwd = os.getcwd()
    config_path = os.path.join(cwd, config_file_name)
    floor_map = fromFile(config_path)
except FileNotFoundError:
    print('specify valid map path')
    sys.exit(0)
options = []

if len(sys.argv) > 2:
    option = sys.argv[2]
    if option in ['--read']:
        if len(sys.argv) > 3:
            source_file_name = sys.argv[3]
            source_path = os.path.join(cwd, source_file_name)
            print('drawing from source')
            simulation = SimulationDrawer(floor_map)
            simulation.draw_from_file(source_path)
            sys.exit(0)
        else:
            print('specify path to source file')
            sys.exit(0)
    if option in ['--headless']:
        options.append(option)

print('running simulation')
simulation = Simulation(floor_map, options)
simulation.run_simulation()
