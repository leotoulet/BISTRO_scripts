import matplotlib.pyplot as plt
import numpy as np
import os
from math import *
import sys 

sys.path.append(os.path.abspath("../fixed_data/"))
from KPIS import *

sys.path.append(os.path.abspath("../utilities/"))
from Sample import *
from collect_inputs import *

MIN_X = 676949
MAX_X = 689624

MIN_Y = 4818750
MAX_Y = 4832294

def KPI_wrt_price_area(samples, standards, KPI, name, folder):

	plt.clf()

	print("    Generating "+name+" wrt to price area")

	price_area = [np.pi*s.road_pricing["r"]**2*s.road_pricing["p"] for s in samples]
	scores = [computeWeightedScores(s, standards, KPI)[-1] for s in samples]

	plt.title(name + "w.r.t price * area")
	plt.xlabel("Price * Area ($ * m^2)")
	plt.ylabel("KPI score")

	plt.plot(price_area, scores, "bo")
	path = folder+"/"+name+"_price_area.png"
	plt.savefig(path)
	print("    Saved to "+path)


def mode_choice_wrt_price_area(samples, standards, mode, name, folder):

	plt.clf()

	print("    Generating "+ name + " choice wrt to price area")

	price_area = [np.pi*s.road_pricing["r"]**2*s.road_pricing["p"] for s in samples]
	scores = [s.mode_split[name] for s in samples]

	plt.title(name + " mode split w.r.t price * area")
	plt.xlabel("Price * Area ($ * m^2)")
	plt.ylabel(name + " mode split")

	plt.plot(price_area, scores, "bo")
	path = folder+"/"+name+"_price_area.png"
	plt.savefig(path)
	print("    Saved to "+path)

