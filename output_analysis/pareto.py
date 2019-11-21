from Sample import *
from collect_inputs import *
from KPIS import *
import matplotlib.pyplot as plt

KPI1 = congestion_KPI
KPI2 = TollRevenue_KPI
KPI1_name = "congestion"
KPI2_name = "tolls"

def swap(list, i, j):
	a = list[i]
	list[i] = list[j]
	list[j] = a

def sort(liste, fun):
	l = len(liste)
	for i in range(l-1):
		for j in range(l-1):
			if inferior(liste[j+1], liste[j]):
				swap(liste, j, j+1)

def pareto_front():
	samples = create_samples_list()
	standards = loadStandardization()

	points = [] #A point is made of a triplet (s, KPI1, KPI2)
	for s in samples:
		congestion = computeWeightedScores(s, standards, KPI1)[-1]
		social = computeWeightedScores(s, standards, KPI2)[-1]
		points.append((s, congestion, social))


	non_pareto = []
	pareto = []

	for p in points:
		pa = True
		for q in points:
			if dominates(q[1:], p[1:]):
				non_pareto.append(p)
				pa = False
				continue
		if pa:
			pareto.append(p)

	sort(pareto, inferior)
	return (pareto, non_pareto)



def dominates(k1, k2):
	#K1 dominates k2 if k1_i <= k2_i for all i and at least one ineq is strict
	one_strict = False

	for i in range(len(k1)):
		if k1[i] > k2[i]:
			return False
		if k1[i] < k2[i]:
			one_strict = True

	return one_strict

def inferior(par1, par2):
	standards = loadStandardization()
	x1 = computeWeightedScores(par1[0], standards, KPI1)[-1]
	y1 = computeWeightedScores(par1[0], standards, KPI2)[-1]
	x2 = computeWeightedScores(par2[0], standards, KPI1)[-1]
	y2 = computeWeightedScores(par2[0], standards, KPI2)[-1]

	if x1 < x2:
		return True
	if x1 > x2:
		return False
	else:
		if y1 < y2:
			return True
		else:
			return False

def plot_pareto(plot = True):
	pareto, non_pareto = pareto_front()

	plt.clf()

	for p in pareto:
		plt.plot(p[1], p[2], 'ro')
		print(p[0].directory, p[0].road_pricing)

	if plot == False:
		return

	for p in non_pareto:
		plt.plot(p[1], p[2], 'xb')

	for i in range(len(pareto) - 1):
		plt.plot([pareto[i][1], pareto[i+1][1]], [pareto[i][2], pareto[i+1][2]],color="black")

	x_min = min(p[1] for p in pareto + non_pareto)
	x_max = max(p[1] for p in pareto + non_pareto)
	y_min = min(p[2] for p in pareto + non_pareto)
	y_max = max(p[2] for p in pareto + non_pareto)

	plt.plot([x_min, x_min], [pareto[0][2], 1000], color='black')
	plt.plot([pareto[len(pareto) - 1][1], 100], [y_min, y_min], color='black')

	plt.xlim((x_min - 0.4, x_max + 0.4))
	plt.ylim((y_min - 0.4, y_max + 0.4))
	plt.xlabel(KPI1_name)
	plt.ylabel(KPI2_name)
	plt.title("Pareto front")

	plt.savefig("pareto.png")

if __name__ == "__main__":
	plot_pareto()