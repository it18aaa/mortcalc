#!/bin/env python
from mort import *

import matplotlib.pyplot as plt

mort_years = 25
principal = 145000
int_rate = 7.99

# calc the repayment amount
repayment = calcRepayment(12 * mort_years, principal, int_rate)
graphData = getGraphData(12 * mort_years, principal, int_rate)

owed = list()
running_total_int = list()
running_total_cap = list()
running_total_all = list()
owed.append(principal)
running_total_cap.append(0)
running_total_int.append(0)
running_total_all.append(0)

totint = 0
totcap = 0

for month in graphData:
    
    #print("{0} £{1} £{2} £{3}".format(month[0], month[1], month[2], month[3])) 

    totint += month[1]
    totcap += month[2]
    #if int(month.get("number")) % 12 == 0:
    owed.append(month[0])
    running_total_cap.append(totcap)
    running_total_int.append(totint)
    running_total_all.append(totcap + totint)

print("repayment "  + str(repayment))

plt.figure()
plt.title('mortgage calc')
plt.plot(owed, 'r-')
plt.axis([0,300,0, principal*2])
plt.ylabel('amount')
plt.xlabel('month')
plt.plot(running_total_int, 'b')
plt.plot(running_total_cap, 'g')
plt.plot(running_total_all, 'y--')
plt.grid(True, which='both')
plt.minorticks_on()


plt.show()
