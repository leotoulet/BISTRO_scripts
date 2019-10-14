from navigate_data import *
##### The next few function all take a folder as input and extract input info


#Load weights from working directory
def load_weights():
	dict_name = "scoringWeights.csv"
	dic = {}
	with open(dict_name) as csvfile:
		df = pd.read_csv(csvfile)
		kpi_names = list(df.columns)
		for name in kpi_names:
			dic[name] = list(df[name])[0]
	return dic


#Reads transit fare inputs
def getTransitFareInputs(tpe_dir):
	path = os.path.join(getInputsDir(tpe_dir), "MassTransitFares.csv")	
	dic = {}
	with open(path) as csvfile:
		df = pd.read_csv(csvfile, index_col=2)
		dic["AdultFare"] = df["amount"][0]
		dic["ChildrenFare"] = df["amount"][1]
		return dic

#Loads the dicationnary of {KPI: mean, std} from working directory
def loadStandardization():
	dict_name = "standardizationParameters.csv"
	params = {}
	with open(dict_name) as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			params[row[0]] = (float(row[1]), float(row[2]))
	return params



#Reads road pricing information inputs
def getRoadPricing(tpe_dir):
	return

def reconstructRoadPrincingArea(tpe_dir):
	return
