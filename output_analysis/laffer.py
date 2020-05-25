from Sample import *
from collect_inputs import *
from collect_outputs import *
from Sample import *
from KPIS import *
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import sys

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
file = open(os.path.join(dir_path,"unstd_bau.csv"))
df = pd.read_csv(file, index_col = "KPI")

# THINGS I CHANGED
# collect_outputs.py: VEHICLES variable, getModeSplit line
# graphing.py: added laffer, commented out other graphs
# laffer.py: created file

def compute_laffer(samples, standards):
	global sample_index
	sample_index = 0

	toll_revenues = []
	car_ridehail_VMTs = []
	equivalent_tax_rates = []
	road_prices = []
	tolled_VMTs = []
	tolled_VMTs_per_trip = []
	VMT_ratio = []
	toll_eligible_trips = []
	# maybe change to be ndarray zeros
	# then update by index in loop, leave as 0 if sample error

	for s in samples:
		#print(sample_index)
		price = s.road_pricing["p"]
		#print("ROAD PRICE: " + str(price))
		trips = s.mode_split.get("ride_hail", 0) + s.mode_split.get("car", 0)

		if len(s.KPIS["TollRevenue"]) == 0:
			tr = 0.0
		else:
			tr = s.KPIS["TollRevenue"][-1]
		#print("TOTAL REVENUE: " + str(tr))
		
		if len(s.KPIS["VMT"]) == 0:
			car_ridehail_vmt = 0.0
		else:
			car_ridehail_vmt = s.KPIS["VMT"][-1]
		#print("CAR-RIDEHAIL VMT: " + str(car_ridehail_vmt))

		if car_ridehail_vmt == 0:
			equivalent_tax_rate = 0.0
		else:
			equivalent_tax_rate = tr / car_ridehail_vmt

		# tolled vmt = vmt within cordon
		if tr == 0:
			tolled_VMT = 0.0
		else:
			tolled_VMT = tr / price
		
		# avg_tolled_VMT_per_trip = tolled_VMT / trips
		# ratio = tolled_VMT / car_ridehail_vmt

		#print("EQUIV TAX RATE: " + str(equivalent_tax_rate))
		#print("TOLLED VMT: " + str(tolled_VMT))

		toll_revenues.append(tr)
		equivalent_tax_rates.append(equivalent_tax_rate)
		road_prices.append(price)
		car_ridehail_VMTs.append(car_ridehail_vmt)
		tolled_VMTs.append(tolled_VMT)
		toll_eligible_trips.append(trips)
		# tolled_VMTs_per_trip.append(avg_tolled_VMT_per_trip)
		# VMT_ratio.append(ratio)
		sample_index += 1

	sample_indices = list(range(sample_index))

	data = list(zip(toll_revenues, equivalent_tax_rates, road_prices, car_ridehail_VMTs, toll_eligible_trips))
	colnames = ["toll_revenue","equivalent_tax_rate","road_price","car_ridehail_VMT", "toll_eligible_trips"]
	df = pd.DataFrame(data, index=sample_indices, columns=colnames)
	return df



def save_laffer_csv(df, folder):
	# data should be list of lists
	# each of length num_samples
	path = folder+"/laffer_data.csv"
	file = open(path, "w")
	# write column names
	# file.write("sample_index,toll_revenue,equivalent_tax_rate,road_price,car_ridehail_VMT,VMT_ratio,tolled_VMT_per_trip\n")
	# for s in zip(data):
	# 	# write data
	# 	for item in s:
	# 		file.write(item+",")
	# 	file.write("\n")
	df.to_csv(path)
	print("    Saved laffer data to: "+path)


def plot_laffer(samples, standards, folder, KPIS, KPIS_names):
	# try:
	
	laffer_data = compute_laffer(samples, standards) # list of lists
	# optimal_sample_index = np.argmax(toll_revenues)

	# print("Optimal Sample Index: " + str(optimal_sample_index))
	# print("TR: " + str(toll_revenues[optimal_sample_index]))
	# print("Equivalent Tax Rate: " + str(tax_rates[optimal_sample_index]))

	#Get best point for each Aggregate KPI
	dic = {}
	for k,n in zip(KPIS, KPIS_names):
		if n[:3] == "Agg":
			best_sample = np.argmin([computeWeightedScores(s, standards, k)[-1] for s in samples])
			dic[n] = samples[best_sample], computeWeightedScores(samples[best_sample], standards, k)[-1]
	print(dic)


	

	plt.clf()
	TR = list(laffer_data["toll_revenue"])
	ETR = list(laffer_data["equivalent_tax_rate"])
	plt.plot(ETR, TR, "ob")
	plt.savefig(folder+"/laffer.png")
	print("    Saved laffer curve plot to: "+folder+"/laffer.png")
	# except Exception as e:
	# 	print("    Failed at creating Laffer Curve " + str(e))
	# 	exc_type, exc_obj, exc_tb = sys.exc_info()
	# 	print("    Line number: " + str(exc_tb.tb_lineno))
	# 	print("    Exception type: " + str(exc_type))
	# 	print("    sample_index: " + str(sample_index))
	# 	pass