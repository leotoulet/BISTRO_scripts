from Sample import *
from collect_inputs import *
from KPIS import *
import matplotlib.pyplot as plt


def pareto_front():
	samples = create_samples_list()
	standards = loadStandardization()

	points = [] #A point is made of a triplet (s, KPI1, KPI2)
	for s in samples:
		congestion = computeWeightedScores(s, standards, congestion_KPI)[-1]
		social = computeWeightedScores(s, standards, social_KPI)[-1]
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


def plot_pareto():
	pareto, non_pareto = pareto_front()

	plt.clf()
	plt.xlim((-1.2, -0.4))
	plt.ylim((-1.2, -0.4))
	plt.xlabel("congestion")
	plt.ylabel("social")
	plt.title("Pareto front")


	for p in pareto:
		plt.plot(p[1], p[2], 'bo')
		print(p[0].road_pricing)

	for p in non_pareto:
		plt.plot(p[1], p[2], 'ro')

	plt.savefig("pareto.png")