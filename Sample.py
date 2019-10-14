#Defines a Sample class that stores all relevant information about a sample
from navigate_data import *
from collect_inputs import *
from collect_outputs import *

class Sample:

	directory = None; #Top level directory of the sample point
	timeStamp = None;
	n_iters = None; #Number of iterations of a sample

	#Inputs
	mass_transit_fares = {"AdultFare":None, "ChildrenFare":None};
	road_pricing = {"x":None, "y":None, "p":None};

	#Outputs
	KPIS = None; #dict of {KPI: (it0, it1, ..., it.n)}
	mode_split = None;	

	def __str__(self):
		return "Sample at directory: " + self.directory + ", at timeStamp: " + str(self.timeStamp)


def init_sample(tpe_dir):
	s = Sample()
	s.directory = tpe_dir
	s.timeStamp = round(read_timestamp(tpe_dir))

	s.mass_transit_fares = getTransitFareInputs(tpe_dir)
	s.mode_split = getModeSplit(tpe_dir)
	s.road_pricing = reconstructRoadPrincingArea(tpe_dir)
	#No road pricing yet

	s.KPIS = retrieve_KPIs(tpe_dir)

	return s

#Returns a list score stored by iteration number
def computeWeightedScores(s, standards, weights):
	kpis_dict = s.KPIS

	scores = []
	iters = kpis_dict['Iteration']
	for i in iters:
		s = 0
		nb_params = 0
		for k in weights:
			nb_params+=1
			w = weights[k]
			mean, std = standards[k]
			value = kpis_dict[k][i]
			s += w*(value - mean)/std
		scores.append(s/sum(weights.values()))

	return scores	


#Returns a list of samples ordered by timeStamp
def create_samples_list(dirs = None):

	if dirs == None:
		dirs = getTimeSortedDirs()

	samples = []

	for d in dirs:
		s = init_sample(d)
		samples.append(s)

	return samples