import yaml
import sys
import os

print("##################### Starting... #####################\n")

############################## Load scripts ################################
sys.path.append(os.path.abspath("./fixed_data/"))
sys.path.append(os.path.abspath("./utilities/"))
sys.path.append(os.path.abspath("./output_analysis/"))
sys.path.append(os.path.abspath("./modeling/"))
from collect_inputs import *
from heatmaps import *
from Sample import *

print("################### Scripts loaded ! ##################\n")


############################ Load configuration file #######################

CONFIG_PATH = "settings.yaml"
CONFIG = None

with open(CONFIG_PATH, 'r') as settings_file:
	CONFIG = yaml.safe_load(settings_file)
assert(CONFIG != None)

print("############ Configuration file loaded ! ##############\n")


########################## Load samples and standards ########################

samples = create_samples_list(CONFIG["EXPERIMENT_DIR"])
standards = load_standards("fixed_data/standardizationParameters.csv")

print("########### Loaded all samples in order ! #############\n")


################################# KPIS ######################################

from KPIS import *
KPIS = ALL_KPIS
KPIS_names = ALL_NAMES

print("#################### Setup finished ###################\n")

######################### USER DEFINED FUNCTIONS #############################

print("Generating score heatmaps for all KPIS")
saving_dir = CONFIG["OUTPUT_DIR"]+"/heatmaps"
for k,n in zip(KPIS, KPIS_names):
	plotTrafficCirclesHeatMap(samples, standards, k, n, )