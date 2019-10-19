########################################################
"""

This script parses the output of the bistro hyperopt optimizater :



"""
########################################################
import os
import sys
import csv
import matplotlib.pyplot as plt
import numpy as np

#Get the current working directory
def get_dir():
	return os.getcwd()

#Get only subdir
def only_subdir(current_dir = os.getcwd()):
	return next(os.walk(current_dir))[1][0]

#Get a list of all subdirectories
def sub_list(current_dir = os.getcwd()):
	return [dir for dir in next(os.walk(current_dir))[1] if dir[0]=='5']

#Get the path of the result file given a TPE folder
def get_results_dir(dir):
	abs_path = os.path.join(get_dir(), dir)
	abs_path = os.path.join(abs_path, 'output')
	abs_path = os.path.join(abs_path, only_subdir(abs_path))
	abs_path = os.path.join(abs_path, only_subdir(abs_path))
	abs_path = os.path.join(abs_path, only_subdir(abs_path))
	abs_path = os.path.join(abs_path, 'competition')
	return abs_path


def read_scores(tpe_dir):
	results_dir = get_results_dir(tpe_dir)
	outfile = os.path.join(results_dir, "submissionScores.csv")
	
	df = pd.read_csv(outfile)
    scores = df["Weighted Score"]
    return score_average(scores)


def score_average(scores):
    congestion = (scores[TMV] + scores[AVG_DELAY] + scores[GHG])/3
    social = (scores[WORK_BURDEN] + scores[BUS_CROWDING])/2
    return (congestion + social)/2

def read_timestamp(tpe_dir):
	results_dir = get_results_dir(tpe_dir)
	outfile = os.path.join(results_dir, "submissionScores.csv")
	timestamp = os.path.getmtime(outfile)
	return timestamp

def check_file_existence(tpe_dir):
	return os.path.exists(os.path.join(get_results_dir(tpe_dir), "submissionScores.csv"))

#Returns array of (timestamp, score)
def read_sorted_tpe_results():
	results = []
	for dir in sub_list():
		if check_file_existence(dir):
			results.append((read_timestamp(dir), read_scores(dir)))
	return sorted(results,key = lambda x:x[0])

def graph_tpe_results():
	plt.cla()
	results = [r[1] for r in read_sorted_tpe_results()]
	order = [i for i in range(len(results))]
	mini = [results[0]]+[min(results[:i]) for i in range(1, len(results))]
	
	plt.xlabel('Trial Number')
	plt.ylabel('Score')

	plt.plot(order, results, 'bo', label='TPE data points')
	plt.plot(order, mini, '--r', label='TPE progress')
	plt.legend(loc='upper right',frameon=True,framealpha=1.0)
	plt.savefig("tpe_score_evolution.png")

def graph_tpe_spread():
	plt.cla()
	results = [r[1] for r in read_sorted_tpe_results()]
	order = [i for i in range(len(results))]
	mini = [results[0]]+[min(results[:i]) for i in range(1, len(results))]
	maxi = [results[0]]+[max(results[:i]) for i in range(1, len(results))]
	mean = [results[0]]+[np.mean(results[max(i-30,0):i]) for i in range(1, len(results))]
	med = [results[0]]+[np.median(results[max(i-30,0):i]) for i in range(1, len(results))]

	plt.plot(order, results, 'bo', alpha=0.2, label='TPE data points')
	plt.plot(order, mini, 'g', label='TPE min')
	plt.plot(order, maxi, 'r', label='TPE max')
	plt.plot(order, mean, 'm', label='TPE mean (last 30 its)')
	plt.plot(order, med, 'y', label='TPE median (last 30 its)')

	plt.xlabel('Trial Number')
	plt.ylabel('Score')

	plt.legend(loc='upper right',frameon=True,framealpha=1.0)

	plt.savefig("tpe_score_spread.png")



if __name__ == "__main__":
	graph_tpe_results()
	graph_tpe_spread()
	