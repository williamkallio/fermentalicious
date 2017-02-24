#WK 2/13/2017
#Utility for calculating fermentation things (ABV, Plato)

#boto3/dynamodb doesn't like floats. Hence using python to convert back to strings
from decimal import *

def calculate_abv(original_gravity, specific_gravity):

    return (Decimal(original_gravity) - Decimal(specific_gravity)) * Decimal(131.25)
