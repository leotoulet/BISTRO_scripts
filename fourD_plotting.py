from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from Sample import *
import matplotlib as mp

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
	samples = create_samples_list()
	weights = load_weights()
	standards = loadStandardization()

	title = "Road pricing as function fo (x,y,p)"

	xi = []
	yi = []
	pi = []
	si = []

	for s in samples:
		si.append(computeWeightedScores(s, standards, weights)[-1])
		xi.append(s.road_pricing["x"])
		yi.append(s.road_pricing["y"])
		pi.append(s.road_pricing["p"])

	scatterAllPoints(xi, yi, pi, si, title)



def scatterAllPoints(xi, yi, zi, vi, title):

	plt.clf()

	fig = plt.figure()
	ax = plt.axes(projection='3d')
	ax.set_title(title)
	ax.set_xlabel('x')
	ax.set_ylabel('y')
	ax.set_zlabel('p')

	maxi = np.max(vi)
	mini = np.min(vi)

	for x,y,z,v in zip(xi, yi, zi, vi):
		ratio = (v - mini)/(maxi - mini)
		color = (0, 1-ratio, ratio, 0.5)
	
	cmap = mp.cm.get_cmap('viridis')
	normalize = mp.colors.Normalize(vmin=min(vi), vmax=max(vi))
	colors = [cmap(normalize(value)) for value in vi]

	ax.scatter(xi, yi, zi, color=colors)

	# Optionally add a colorbar
	cax, _ = mp.colorbar.make_axes(ax)
	cbar = mp.colorbar.ColorbarBase(cax, cmap=cmap, norm=normalize)

	plt.savefig("scatterAllPoints.png")	


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


