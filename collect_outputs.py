from naviage_data.py import *


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

	with open(path) as csvfile:
		df = pd.read_csv(csvfile)
		kpi_names = list(df.columns)
		for name in kpi_names:
			dic[trans_dict[name]] = list(df[name])
	return dic


