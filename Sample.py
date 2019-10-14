#Defines a Sample class that stores all relevant information about a sample

class Sample:

	directory = None; #Top level directory of the sample point
	n_iters = None; #Number of iterations of a sample

	#Inputs
	mass_transit_fares = {"AdultFare":None, "ChildrenFare":None};
	road_pricing = {};

	#Outputs
	KPIS = None; #dict of {KPI: (it0, it1, ..., it20)}	
