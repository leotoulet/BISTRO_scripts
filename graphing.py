import yaml
import sys
import os

print("Starting...\n")

############################## Load scripts ################################
sys.path.append(os.path.abspath("./fixed_data/"))
sys.path.append(os.path.abspath("./utilities/"))
sys.path.append(os.path.abspath("./output_analysis/"))
sys.path.append(os.path.abspath("./modeling/"))
from collect_inputs import *
from heatmaps import *
from Sample import *

print("Scripts loaded !")


############################ Load configuration file #######################

CONFIG_PATH = "settings.yaml"
CONFIG = None

with open(CONFIG_PATH, 'r') as settings_file:
	CONFIG = yaml.safe_load(settings_file)
assert(CONFIG != None)

CONFIG["EXPERIMENT_DIR"] = os.path.abspath(CONFIG["EXPERIMENT_DIR"])
CONFIG["OUTPUT_DIR"] = os.path.abspath(CONFIG["OUTPUT_DIR"])

print("Configuration file loaded !")


########################## Load samples and standards ########################

samples_time_sorted = create_samples_list(CONFIG["EXPERIMENT_DIR"])
standards = load_standards("fixed_data/standardizationParameters.csv")

print("\nLoaded all samples in order !")


################################# KPIS ######################################

from KPIS import *
KPIS = ALL_KPIS
KPIS_names = ALL_NAMES

######################### USER DEFINED FUNCTIONS #############################

for k,n in zip(KPIS, KPIS_names):
	plotTrafficCirclesHeatMap(k, n, CONFIG["OUTPUT_DIR"]+"heatmaps/")