
import numpy as np
import scipy

def get_pmcc(twoVars: list) -> float:
	"""
	Takes in a list of ordered pairs (x,y), returns
	the Pearson product-moment correlation
	coefficient describing the relationship
	between x and y.
	"""
	
	xArray = np.array([entry[0] for entry in twoVars])
	yArray = np.array([entry[1] for entry in twoVars])

	if len(xArray) < 2 or len(yArray) < 2:
		return None

	resultObj = scipy.stats.pearsonr(xArray, yArray)

	return resultObj.correlation


print(get_pmcc([(1, 2), (4, 8), (9, 7), (11, 10)]))

# https://support.minitab.com/en-us/minitab/21/help-and-how-to/statistics/basic-statistics/how-to/correlation/methods-and-formulas/methods-and-formulas/#pearson-s-correlation-coefficient
