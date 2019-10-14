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

##CREATE COLOR MAPS
def customColorMap(r, g, b, a):
	colors = [(r, g, b, a), [r, g ,b, a]]  # R -> R
	n_bin = 10  # Discretizes the interpolation into bins
	cmap_name = 'my_list'
	cm = LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bin)
	return cm


def f(x, y, z):
    return (x ** 2 + y ** 2 - z ** 2)

def scatterRoadPricing():

	os.makedirs("4DPlots",exist_ok=True)

	samples = create_samples_list()
	weights = load_weights()
	standards = loadStandardization()

	title = " = f(x,y,p)"

	xi = []
	yi = []
	pi = []
	si = []

	for s in samples:
		xi.append(s.road_pricing["x"])
		yi.append(s.road_pricing["y"])
		pi.append(s.road_pricing["p"])

	KPIS = list(weights.keys())
	for k in KPIS:
		si = []
		for s in samples:
			si.append(computeWeightedScores(s, standards, singleKPI_weights(k))[-1])

		scatterAllPoints(xi, yi, pi, si, k + title)

	si = []
	for s in samples:
		si.append(computeWeightedScores(s, standards, weights)[-1])
	scatterAllPoints(xi, yi, pi, si, "Aggregate" + title)



def scatterAllPoints(xi, yi, zi, vi, title):

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

	fn = get_sample_data(os.path.join(os.getcwd(),"map.png"), asfileobj=False)
	arr = read_png(fn)
	# 10 is equal length of x and y axises of your surface
	stepX = (max(xi) - min(xi)) / arr.shape[0] - 1
	stepY = (max(yi) - min(yi)) / arr.shape[1] - 1

	X1 = np.arange(min(xi), max(xi), stepX)
	Y1 = np.arange(min(yi), max(yi), stepY)
	X1, Y1 = np.meshgrid(X1, Y1)
	Z = np.zeros(X1.shape)
	# stride args allows to determine image quality 
	# stride = 1 work slow
	ax.plot_surface(X1, Y1, Z, rstride=1, cstride=1, facecolors=arr)




	plt.savefig("4DPlots/" + title + "__scatterAllPoints.png")


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


