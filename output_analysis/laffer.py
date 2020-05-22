from Sample import *
from collect_inputs import *
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
	# maybe change to be ndarray zeros
	# then update by index in loop, leave as 0 if sample error

	for s in samples:
		print(sample_index)
		price = s.road_pricing["p"]
		toll_eligible_trips = s.mode_split.get("ride_hail", 0) + s.mode_split.get("car", 0)
		tr = s.KPIS["TollRevenue"][-1]
		car_ridehail_vmt = s.KPIS["VMT"][-1]

		equivalent_tax_rate = tr / car_ridehail_vmt
		tolled_VMT = car_ridehail_vmt / tr
		avg_tolled_VMT_per_trip = tolled_VMT / toll_eligible_trips
		ratio = tolled_VMT / car_ridehail_vmt

		toll_revenues.append(tr)
		equivalent_tax_rates.append(equivalent_tax_rate)
		road_prices.append(price)
		car_ridehail_VMTs.append(car_ridehail_vmt)
		tolled_VMTs.append(tolled_VMT)
		tolled_VMTs_per_trip.append(avg_tolled_VMT_per_trip)
		VMT_ratio.append(ratio)
		sample_index += 1

	sample_indices = list(range(sample_index))

	data = list(zip(toll_revenues, equivalent_tax_rates, road_prices, car_ridehail_VMTs, VMT_ratio, tolled_VMTs_per_trip))
	colnames = ["toll_revenue","equivalent_tax_rate","road_price","car_ridehail_VMT","VMT_ratio","tolled_VMT_per_trip"]
	df = pd.DataFrame(data, index=sample_indices, columns=colnames)
	return df



def save_laffer_csv(df, folder):
	# data should be list of lists
	# each of length num_samples
	path = folder+"/laffer.csv"
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


def plot_laffer(samples, standards, folder):
	# try:
	print("    Generating Laffer Curve")
	
	laffer_data = compute_laffer(samples, standards) # list of lists
	optimal_sample_index = np.argmax(toll_revenues)

	print("Optimal Sample Index: " + str(optimal_sample_index))
	print("TR: " + str(toll_revenues[optimal_sample_index]))
	print("Equivalent Tax Rate: " + str(tax_rates[optimal_sample_index]))

	save_laffer_csv(laffer_data, folder)

	plt.clf()


	# except Exception as e:
	# 	print("    Failed at creating Laffer Curve " + str(e))
	# 	exc_type, exc_obj, exc_tb = sys.exc_info()
	# 	print("    Line number: " + str(exc_tb.tb_lineno))
	# 	print("    Exception type: " + str(exc_type))
	# 	print("    sample_index: " + str(sample_index))
	# 	pass