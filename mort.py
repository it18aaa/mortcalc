#!/bin/env python
# Mortgage repayment calculator
# Using using formulae from http://motgagesexposed.com
# I Thomson
#

from decimal import Decimal


# 
#
def calcRepayment(num_repayments, principal, yearly_rate):
    pv = principal
    i = (yearly_rate / 12) / 100
    n = num_repayments
    #pmt = (i * pv) * (1 + i)**n / ((1 + i)**n) - 1 
    pmt = pv * i / (1-(1+i)**-n)
    return round(Decimal(pmt), 2)

# calculate the capital at any point during repayment, given repayment amount
#
def calcFutureValue(num_repayments, principal, yearly_rate, repayment):
    i = (yearly_rate / 12) / 100
    pv = principal
    n = num_repayments
    pmt = float(repayment)

    fv = pv * (1 + i)**n - pmt * (((1 + i)**n)-1) / i
    return round(Decimal(fv), 2)


# example values to demo
mort_years = 25
principal = 145000
int_rate = 2.99

# calc the repayment amount
repayment = calcRepayment(12 * mort_years, principal, int_rate)

# iterate through values and print out details:-
lastval = 0
inttot= Decimal(0)
for i in range(1, 12*mort_years+1):
    val = Decimal(calcFutureValue(i, principal, int_rate, repayment))
    if (lastval != 0):
        capital = lastval - val
    else:
        capital = principal - val

    interest = repayment - capital
    capperc = round(Decimal((capital / repayment)*100), 1)
    intperc = round(Decimal((interest / repayment) * 100), 1)
    inttot += interest
    print("{0}. {1} -  £{2} ({3}%) £{4} ({5}%)  inttot: £{6}".format(
        i, val, capital, capperc, interest, intperc, inttot))        
    lastval = Decimal(val)    
    

total_repayment = repayment * 12 * mort_years
print("Monthly Repayment: £ {0} ".format(repayment))
print("Total Repaid:  £ {0} ".format(total_repayment))
