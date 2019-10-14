from navigate_data import *
##### The next few function all take a folder as input and extract input info

#Since not all csv files share the same KPI headers, and tranlsation dictionnary is in order
trans_dict = {

	'Iteration':'Iteration',

	'Accessibility: number of secondary locations accessible by car within 15 minutes':'driveSecondaryAccessibility',
	'Accessibility: number of secondary locations accessible by transit within 15 minutes':'transitSecondaryAccessibility',
	'Accessibility: number of work locations accessible by car within 15 minutes':'driveWorkAccessibility',
	'Accessibility: number of work locations accessible by transit within 15 minutes':'transitWorkAccessibility',

	'Congestion: average vehicle delay per passenger trip':'averageVehicleDelayPerPassengerTrip',
	'Congestion: total vehicle miles traveled':'motorizedVehicleMilesTraveled_total',
	'Equity: average travel cost burden -  secondary':'averageTravelCostBurden_Secondary',
	'Equity: average travel cost burden - work':'averageTravelCostBurden_Work',
	'Level of service: average bus crowding experienced':'busCrowding',
	'Level of service: costs and benefits':'costBenefitAnalysis',

	'Sustainability: Total grams GHGe Emissions':'sustainability_GHG',
	'Sustainability: Total grams PM 2.5 Emitted':'sustainability_PM'
}



#Reads transit fare inputs
def getTransitFareInputs(tpe_dir):
	path = os.path.join(getInputsDir(tpe_dir), "MassTransitFares.csv")	
	dic = {}
	with open(path) as csvfile:
		df = pd.read_csv(csvfile, index_col=2)
		dic["AdultFare"] = df["amount"][0]
		dic["ChildrenFare"] = df["amount"][1]
		return dic


#Reads road pricing information inputs
def getRoadPricing(tpe_dir):
	return

def reconstructRoadPrincingArea(tpe_dir):
	return
