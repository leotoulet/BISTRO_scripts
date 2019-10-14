import os
import sys
import csv
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import random
from scipy.interpolate import griddata
import numpy as np

#### The next few functions help navigate data points directories

#Get the current working directory
def get_dir():
	return os.getcwd()

#Get only subdir of a directory
def only_subdir(current_dir = os.getcwd()):
	return next(os.walk(current_dir))[1][0]

#Get a list of all subdirectories
def sub_list(current_dir = os.getcwd()):
	return [dir for dir in next(os.walk(current_dir))[1] if dir[0]=='5' and check_file_existence(dir)]

#Read the timestamp of a data point
def read_timestamp(tpe_dir):
	results_dir = get_results_dir(tpe_dir)
	outfile = os.path.join(results_dir, "submissionScores.csv")
	timestamp = os.path.getmtime(outfile)
	return timestamp

#Check data existence and input validity
def check_file_existence(tpe_dir):
	outputs =  os.path.exists(os.path.join(get_results_dir(tpe_dir), "submissionScores.csv"))
	inputs = os.path.exists(os.path.join(getInputsDir(tpe_dir), "MassTransitFares.csv"))
	return inputs and outputs

#Return a list of data points sorted by time
def getTimeSortedDirs():
	dirs = sub_list()
	dirs = sorted(dirs, key = lambda x:read_timestamp(x))
	print("Number of complete result directories : "+str(len(dirs)))
	return dirs

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

def getInputsDir(tpe_dir):
	abs_path = os.path.join(get_dir(), tpe_dir)
	abs_path = os.path.join(abs_path, 'submission-inputs')
	abs_path = os.path.join(abs_path, only_subdir(abs_path))
	return abs_path


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
