import yaml
import sys
import os

print("Starting...\n")

############################## Load scripts ################################
sys.path.append(os.path.abspath("./fixed_data/"))
sys.path.append(os.path.abspath("./utilities/"))
sys.path.append(os.path.abspath("./output_analysis/"))
sys.path.append(os.path.abspath("./modeling/"))
from heatmaps import *
from Sample import *

print("scripts loaded !")


############################ Load configuration file #######################

CONFIG_PATH = "settings.yaml"
CONFIG = None

with open(CONFIG_PATH, 'r') as settings_file:
	CONFIG = yaml.safe_load(settings_file)
assert(CONFIG != None)

CONFIG["EXPERIMENT_DIR"] = os.path.abspath(CONFIG["EXPERIMENT_DIR"])
CONFIG["OUTPUT_DIR"] = os.path.abspath(CONFIG["OUTPUT_DIR"])

print("Configuration file loaded !")


############################## Load samples #############################

samples_time_sorted = create_samples_list(CONFIG["EXPERIMENT_DIR"])

print("Loaded all samples in order !")