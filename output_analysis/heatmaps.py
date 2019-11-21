from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import matplotlib as mp
import pickle
import os
from matplotlib._png import read_png
from matplotlib.cbook import get_sample_data
import matplotlib.lines as mlines
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

sigmas = []
xcs = []
ycs = []
radius = []


def plotTrafficCirclesHeatMap(samples, standards, KPI, name, folder, f = 2):
	print("    Creating score heatmap for KPI : " + name)

	global sigmas, xcs, ycs
	sigmas = []
	xcs = []
	ycs = []

	X, Y = np.meshgrid(np.linspace(MIN_X, MAX_X, 1000), np.linspace(MIN_Y, MAX_Y, 1000))
	
	for s in samples:
		if s.road_pricing["r"]!=0: # and s.KPIS["TollRevenue"][-1] !=0:
			xcs.append(s.road_pricing["x"])
			ycs.append(s.road_pricing["y"])
			sigmas.append(s.road_pricing["r"]/f)



	si = []
	for s in samples:
		if s.road_pricing["r"]!=0: # and s.KPIS["TollRevenue"][-1] !=0:
			si.append(computeWeightedScores(s, standards, KPI)[-1])
	Z = combined_normal_distribution(X, Y, si)

	fig, ax = plt.subplots()
	z_min, z_max = Z.min(), Z.max()

	Z = (Z - z_min)/z_max

	plotSiouxFauxMap(ax)
	c = ax.pcolormesh(X, Y, Z, cmap='RdBu_r', vmin=0, vmax=1)
	ax.set_title(name)
	# set the limits of the plot to the limits of the data
	ax.axis([X.min(), X.max(), Y.min(), Y.max()])
	fig.colorbar(c, ax=ax)

	filepath = folder+"/score_heatmap_"+name+".png"
	plt.savefig(filepath)
	print("    Saved heatmap to: "+filepath)


def normal_distribution(x,y, xc, yc, sigma):
	r = np.sqrt((x - xc)**2 + (y - yc)**2)
	return np.exp(-r**2/(2*sigma**2))
	return 1/np.sqrt(2*pi*sigma**2)*np.exp(-r**2/(2*sigma**2))


def combined_normal_distribution(x,y, factors):
	global sigmas, xcs, ycs
	value = 0
	for i in range(len(xcs)):
		value += factors[i]/len(factors)*normal_distribution(x,y,xcs[i], ycs[i], sigmas[i])
	return value


def plotSiouxFauxMap(ax):
	for row in load_network():
		if row[0].isdigit():
			fromLocationX,fromLocationY,toLocationX,toLocationY = float(row[-4]),float(row[-3]),float(row[-2]),float(row[-1])
			X = [fromLocationX,toLocationX]
			Y = [fromLocationY, toLocationY]
			plt.plot(X, Y, 'w')