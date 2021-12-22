from simulation.simulation_loop import Simulation
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
floor0 = fromFile(config_path)

simulation = Simulation()
simulation.run_simulation(floor0)