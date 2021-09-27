import math

def getMeanAndVariance(listOfValues):

    # Number of observations
    n = len(listOfValues)

    # Mean of the data
    mean = sum(listOfValues) / n

    # Square deviations
    deviations = [(x - mean) ** 2 for x in listOfValues]

    # Variance
    variance = math.sqrt( sum(deviations) / n )

    return (mean, variance)