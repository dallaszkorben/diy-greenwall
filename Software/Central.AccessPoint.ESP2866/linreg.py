class LinReg():

    def __init__(self, xList, yList):

        n = len(xList)
 
        meanX = self.mean(xList)
        meanY = self.mean(yList)
 
        xMeanList = [a - meanX for a in xList]
        yMeanList = [a - meanY for a in yList]

        numer = sum(self.multiplyLists(xMeanList, yMeanList))
        denom = sum(self.multiplyLists(xMeanList, xMeanList))

        self.m = numer/denom
        self.b = meanY - (self.m * meanX)

    def multiplyLists(self, list1, list2):
        products = []

        for num1, num2 in zip(list1, list2):
            products.append(num1 * num2)
            return products

    def mean(self, lst):
        return sum(lst) / float(len(lst))

#def variance(values, mean):
#    return sum([(x-mean)**2 for x in values])
#
#def covariance(x, mean_x, y, mean_y):
#    covar = 0.0
#    for i in range(len(x)):
#        covar += (x[i] - mean_x) * (y[i] - mean_y)
#    return covar

    def getCoef(self):
        return (self.m, self.b)

    def getY(self, x):
        return self.m * x + self.b
