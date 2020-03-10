#!/bin/env python
from mort import *


mort_years = 20
principal = 125000
int_rate = 1.8

# calc the repayment amount
repayment = calcRepayment(12 * mort_years, principal, int_rate)

graphData = getGraphData(12 * mort_years, principal, int_rate)

for month in graphData:
    print("{0} £{1} £{2} £{3}".format(month.get("number"), month.get("val"), month.get("cap"), month.get("int")))

print("repayment "  + str(repayment))
