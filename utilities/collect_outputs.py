from navigate_data import *
import gzip
import xmltodict

MODE_CHOICES = ['car', 'drive_transit', 'ride_hail', 'walk', 'walk_transit']

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
	'Sustainability: Total grams PM 2.5 Emitted':'sustainability_PM',
	'TollRevenue':'TollRevenue'
}

def read_score(tpe_dir):
	results_dir = get_results_dir(tpe_dir)
	outfile = os.path.join(results_dir, "submissionScores.csv")
	
	with open(outfile) as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			if row[0] == 'Submission Score':
				return round(float(row[-1]), 2)


#Returns a dict of {KPI: (it0, it1, ..., it20)}			
def retrieve_KPIs(tpe_dir):
	path = os.path.join(get_results_dir(tpe_dir), "rawScores.csv")
	dic = {}

	if not check_file_existence(tpe_dir):
		return

	csvfile = open(path)
	df = pd.read_csv(csvfile, index_col="Iteration")
	kpi_names = list(df.columns)
	dic['Iteration'] = [i for i in range(len(df))]
	for name in kpi_names:
		dic[trans_dict[name]] = list(df[name])

	if "TollRevenue" not in dic.keys():
		tolls = get_toll_revenue(tpe_dir)
		dic["TollRevenue"] = [tolls for i in range(31)]
		df.insert(len(df.columns), 'TollRevenue', tolls, allow_duplicates = False)

	csvfile.close()
	df.to_csv(path)
	return dic


def getModeSplit(tpe_dir):
	abs_path = os.path.join(tpe_dir, 'output')
	abs_path = os.path.join(abs_path, only_subdir(abs_path))
	abs_path = os.path.join(abs_path, only_subdir(abs_path))
	abs_path = os.path.join(abs_path, only_subdir(abs_path))
	path = os.path.join(abs_path, "realizedModeChoice.csv")

	dic = {}

	with open(path) as csvfile:
		df = pd.read_csv(csvfile, index_col=0)

		summ = 0
		for col in df.columns:
			summ += list(df[col])[-1]

		for col in df.columns: 
			dic[col] = round(list(df[col])[-1]/summ, 2)

	return dic

def get_toll_revenue(tpe_dir):
	output_dir = os.path.join(tpe_dir, 'output')
	output_dir = os.path.join(output_dir, only_subdir(output_dir))
	output_dir = os.path.join(output_dir, only_subdir(output_dir))
	output_dir = os.path.join(output_dir, only_subdir(output_dir))
	f = gzip.open(os.path.join(output_dir,'outputEvents.xml.gz'), 'rb')
	doc = xmltodict.parse(f.read())
	totalTolls = 0
	for event in doc['events']['event']:
		if '@tollPaid' in event.keys():
			totalTolls += float(event['@tollPaid'])

	print("Tolls paid : " + str(totalTolls)+"\r")
	return totalTolls