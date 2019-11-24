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
from price_area_functions import *
from link_coloring import *
from pareto import *

print("################### Scripts loaded ! ##################\n")


############################ Load configuration file #######################

CONFIG_PATH = "settings.yaml"
CONFIG = None

with open(CONFIG_PATH, 'r') as settings_file:
	CONFIG = yaml.safe_load(settings_file)
assert(CONFIG != None)

os.makedirs(CONFIG["OUTPUT_DIR"], exist_ok = True)

print("############ Configuration file loaded ! ##############\n")


########################## Load samples and standards ########################

samples = create_samples_list(CONFIG["EXPERIMENT_DIR"])
standards = load_standards("fixed_data/standardizationParameters.csv")

def filter(s): #Returns a bool it we want to keep the sample
	return s.mode_split["car"]/sum(list(s.mode_split.values())) > 0.4

samples = [s for s in samples if filter(s)]


print("######## Loaded all " + str(len(samples)) + " samples in order ! ############\n")


################################# KPIS ######################################

from KPIS import *
KPIS = ALL_KPIS
KPIS_names = ALL_NAMES

print("#################### Setup finished ###################\n")

######################### USER DEFINED FUNCTIONS #############################

def price_area():
	samples_copy = [s for s in samples]
	print("Generating price area graphs")
	saving_dir = CONFIG["OUTPUT_DIR"]+"/price_area"
	os.makedirs(saving_dir, exist_ok = True)
	for k,n in zip(KPIS, KPIS_names):
		KPI_wrt_price_area(samples_copy, standards, k, n, saving_dir)

	for k in samples[0].mode_split.keys():
		mode_choice_wrt_price_area(samples_copy, standards, k, k, saving_dir)

def heatmaps():
	samples_copy = [s for s in samples] #Because the function sorts the array in place
	print("Generating score heatmaps for all KPIS")
	saving_dir = CONFIG["OUTPUT_DIR"]+"/heatmaps"
	os.makedirs(saving_dir, exist_ok = True)
	for k,n in zip(KPIS, KPIS_names):
		plotTrafficCirclesHeatMap(samples_copy, standards, k, n, saving_dir)

def link_coloring():
	samples_copy = [s for s in samples]
	print("Generating link coloring graphs")
	saving_dir = CONFIG["OUTPUT_DIR"] + "/link_coloring"
	os.makedirs(saving_dir, exist_ok = True)
	for k,n in zip(KPIS, KPIS_names):
		best_scores_link_congestion(samples_copy, standards, k, n, saving_dir)
		best_scores_link_tolls(samples_copy, standards, k, n, saving_dir)

def pareto():
	samples_copy = [s for s in samples]
	print("Generating pareto fronts")
	saving_dir = CONFIG["OUTPUT_DIR"] + "/pareto"
	os.makedirs(saving_dir, exist_ok = True)
	for k1,n1 in zip(KPIS, KPIS_names):
		for k2, n2 in zip(KPIS, KPIS_names):
			plot_pareto(samples_copy, standards, k1, k2, n1, n2, saving_dir)


#############################################################################

if __name__=="__main__":
	heatmaps()
	#link_coloring()
	pareto()
	price_area()


