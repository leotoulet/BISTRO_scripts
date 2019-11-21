import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
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


def getSiouxFauxLinks():
	rows = []
	avg = 0
	i = 0
	for row in load_network():
		if row[0].isdigit():
			fX,fY,tX,tY = float(row[-4]),float(row[-3]),float(row[-2]),float(row[-1])
			rows.append((fX, fY, tX, tY))
			avg += sqrt((fX-tX)**2+(fY-tY)**2)
			i+=1

	return rows

def best_scores_link_tolls(samples, standards, KPI, name, folder, percent = 0.1):
	links = getSiouxFauxLinks()
	weighted_tolls = [0 for i in range(len(links))]

	print("    Generating best" + name + " avg link tolls")

	samples = sorted(samples, key=lambda x:computeWeightedScores(x, standards, KPI)[-1])
	for s in samples[:int(percent*len(samples))]:
		xc,yc,r = s.road_pricing["x"], s.road_pricing["y"], s.road_pricing["r"]
		p = s.road_pricing["p"]

		for i,l in enumerate(links):
			fX,fY,tX,tY = l
			if (fX - xc)**2 + (fY - yc)**2 < r**2 and (tX - xc)**2 + (tY - yc)**2 < r**2:
				weighted_tolls[i] += p/(percent*len(samples))

	fig, ax = plt.subplots()

	tolls_max = max(weighted_tolls)
	tolls_min = min(weighted_tolls)
	lmin, lmax = None, None

	for i in range(len(links)):
		X = [links[i][0], links[i][2]]
		Y = [links[i][1], links[i][3]]
		c = [1 - (weighted_tolls[i] - tolls_min)/(tolls_max-tolls_min), (weighted_tolls[i] - tolls_min)/(tolls_max-tolls_min), 0]
		if weighted_tolls[i]==tolls_min:
			lmin, = ax.plot(X,Y,color=c, label="min")
		if weighted_tolls[i]==tolls_max:
			lmax, = ax.plot(X,Y,color=c, label="max")
		else:
			ax.plot(X,Y,color=c)

	tolls_min = round(tolls_min, 2)
	tolls_max = round(tolls_max, 2)
	print(tolls_min, tolls_max)
	plt.legend((lmin, lmax), (str(tolls_min)+"$/m", str(tolls_max)+"$/m"))

	plt.title("Average toll " name +", "+ str(int(100*percent)) + "% best samples")
	
	filepath = folder+"/link_coloring_"+name+".png"
	plt.savefig(filepath)
	print("    Saved tollmap to: "+filepath)