from Sample import *

import numpy
import scipy.optimize as optimization


xdata = numpy.array([[0,0], [0,1], [1,0], [1,1], [2,3], [3,2]]).transpose()
ydata = numpy.array([1, 0, 0, 1, 6, 6])


def func(x, *params):
    return params[0]*x[0] + params[1]*x[1] + params[2]*x[0]*x[1]


def fit_input_to_submission_score():
	samples = create_samples_list()
	weights = load_weights()
	standards = loadStandardization()

	xdata = []
	ydata = []

	for s in samples:
		xdata.append([s.mass_transit_fares["AdultFare"], s.mass_transit_fares["ChildrenFare"]])
		ydata.append(computeWeightedScores(s, standards, weights)[-1])

	x0 = np.array([0, 0, 0])
	xdata = np.array(xdata).transpose()
	ydata = np.array(ydata)
	print(xdata)
	print(optimization.curve_fit(func, xdata, ydata, x0))

if __name__ == '__main__':
	fit_input_to_submission_score();