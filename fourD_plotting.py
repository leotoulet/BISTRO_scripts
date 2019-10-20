from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from Sample import *
import matplotlib as mp
import pickle
import os
from matplotlib._png import read_png
from matplotlib.cbook import get_sample_data


NB_GRAPHS = 10 #Used for 5D plots

##CREATE COLOR MAPS
def customColorMap(r, g, b, a):
	colors = [(r, g, b, a), [r, g ,b, a]]  # R -> R
	n_bin = 10  # Discretizes the interpolation into bins
	cmap_name = 'my_list'
	cm = LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bin)
	return cm


def f(x, y, z):
    return (x ** 2 + y ** 2 - z ** 2)

def scatterRoadPricing(): #5d road pricing

	os.makedirs("4DPlots",exist_ok=True)

	samples = create_samples_list()
	weights = load_weights()
	standards = loadStandardization()

	title = " = f(x,y,r,p) "

	xi = []
	yi = []
	ri = []
	pi = []
	si = []

	for s in samples:
		xi.append(s.road_pricing["x"])
		yi.append(s.road_pricing["y"])
		ri.append(s.road_pricing["r"])
		pi.append(s.road_pricing["p"])


	KPIS = list(weights.keys())
	for k in KPIS:
		si = []
		for s in samples:
			si.append(computeWeightedScores(s, standards, singleKPI_weights(k))[-1])


		scatterBinnedPoints(xi, yi, ri, pi, si, k + title + b_string, k)

	si = []
	for s in samples:
		si.append(computeWeightedScores(s, standards, weights)[-1])
	scatterBinnedPoints(xi, yi, ri, pi, si, "Aggregate" + title + b_string, "Aggregate")



def scatterBinnedPoints(xi, yi, zi, ti, vi, title, folder):

	os.makedirs("4DPlots/" + folder, exist_ok=True)

	bins = [min(ti) + i/NB_GRAPHS*(max(ti) - min(ti)) for i in range(NB_GRAPHS)] + [max(pi)]
	for i in range(NB_GRAPHS):
		inf = bins[i]
		sup = bins[i+1]
		b_string = "[" + str(round(inf, 1)) + " ; " + str(round(sup, 1)) + "]"


		x,y,z,v = [],[],[],[]
		for i in range(len(xi)):
			if ti[i] >= inf and ti[i] <= sup:
				x.append(xi[i])
				y.append(yi[i])
				r.append(zi[i])
				s.append(vi[i])

		scatterAllPoints(xi, yi, zi, vi, "Aggregate" + title + b_string, folder)


def scatterAllPoints(xi, yi, zi, vi, title, folder=""):

	plt.clf()

	fig = plt.figure()
	ax = plt.axes(projection='3d')
	ax.set_title(title)
	ax.set_xlabel('x')
	ax.invert_xaxis() #Otherwise 3D projection does not have x and y intersect at their minimum
	ax.set_ylabel('y')
	ax.set_zlabel('p')

	maxi = np.max(vi)
	mini = np.min(vi)
	
	cmap = mp.cm.get_cmap('viridis')
	normalize = mp.colors.Normalize(vmin=min(vi), vmax=max(vi))
	colors = [cmap(normalize(value)) for value in vi]

	ax.scatter(xi, yi, zi, color=colors)

	cax, _ = mp.colorbar.make_axes(ax)
	cbar = mp.colorbar.ColorbarBase(cax, cmap=cmap, norm=normalize)

	plt.savefig("4DPlots/" + folder + "/" + title + ".png")



def scatterByBins():
	#For each X, Y and Z, gets a V value
	points_per_axis = 40

	xs = np.linspace(-6, 6, points_per_axis)
	ys = np.linspace(-6, 6, points_per_axis)
	zs = np.linspace(-6, 6, points_per_axis)
	X,Y,Z = np.meshgrid(xs,ys,zs)
	V = f(X,Y,Z) #30*30*30 array

	#We want to discretize V into several plots of different colors based
	#on the value of V
	nb_bins = points_per_axis
	mini = np.min(V)
	maxi = np.max(V)
	bins = np.linspace(mini, maxi, nb_bins + 1)


	ax.set_xlabel('x')
	ax.set_ylabel('y')
	ax.set_zlabel('z')
	ax.set_xlim3d(-6, 6)
	ax.set_ylim3d(-6, 6)
	ax.set_zlim3d(-6, 6)

	for i in range(nb_bins):
		print("Bin : ",str(i + 1))
		plt.cla()

		ax.set_title('Bin [' + str(round(bins[i], 1)) + " ; " + str(round(bins[i+1], 1)) + "]")
		ax.set_xlabel('x')
		ax.set_ylabel('y')
		ax.set_zlabel('z')
		ax.set_xlim3d(-6, 6)
		ax.set_ylim3d(-6, 6)
		ax.set_zlim3d(-6, 6)

		xi = np.array([])
		yi = np.array([])
		zi = np.array([])
		

		for x in range(points_per_axis):
			for y in range(points_per_axis):
				for z in range(points_per_axis):
					
					if V[x,y,z] > bins[i] and V[x,y,z] <= bins[i+1]:

						xi = np.append(xi,xs[x])
						yi = np.append(yi,ys[y])
						zi = np.append(zi,zs[z])
		
		if len(zi) == 0:
			continue
		ax.scatter(xi, yi, zi, c=[(i/nb_bins,0,1-i/nb_bins,0.3)], vmin=np.nanmin(zi), vmax=np.nanmax(zi))
		plt.savefig("fig"+str(i)+".png")


