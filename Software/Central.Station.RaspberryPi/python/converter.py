import math

class Converter:

    @staticmethod 
    def getLinearValueToExponential(linearValue, maxLinearValue, maxDutyCycle):
        POWER = 80

        # 0 ,,, 1
        normalizedValue = linearValue / maxLinearValue

        # 1 ... POWER -> 0 ,,, (POWER-1)
        expValue = math.pow(POWER, normalizedValue) - 1

        # 0 ... MAX_DUTY_CYCLE
        fadeValue = (int)(maxDutyCycle * expValue / (POWER - 1))

        return fadeValue

