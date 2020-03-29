#!/bin/env python
# Mortgage repayment calculator
# Using using formulae from http://motgagesexposed.com
#
from decimal import Decimal
from PyQt5.QtCore import QDate

#  calculate the repayment based on annual interest rate,
#  principal (money borrowed), and the number of monthly repayments
#
def calcRepayment(num_repayments, principal, yearly_rate):
    pv = principal
    i = (yearly_rate / 12) / 100
    n = num_repayments
    #pmt = (i * pv) * (1 + i)**n / ((1 + i)**n) - 1
    pmt = pv * i / (1-(1+i)**-n)
    return round(Decimal(pmt), 2)

# calculate the future value at any point during repayment, given repayment amount
#
def calcFutureValue(num_repayments, principal, yearly_rate, repayment):
    i = (yearly_rate / 12) / 100
    pv = principal
    n = num_repayments
    pmt = float(repayment)
    fv = pv * (1 + i)**n - pmt * (((1 + i)**n)-1) / i
    return round(Decimal(fv), 2)

def getGraphData(num_repayments, principal, int_rate, start_date):
    repayment = calcRepayment(num_repayments, principal, int_rate)
    # iterate through values and print out details:-
    lastval = 0
    inttot = Decimal(0)
    data = list()
    for i in range(1, num_repayments + 1):
        val = Decimal(calcFutureValue(i, principal, int_rate, repayment))
        if (lastval != 0):
            capital = lastval - val
        else:
            capital = principal - val

        interest = repayment - capital
        inttot += interest
        month_data = [int(i),
                      start_date.addMonths(i).toString('dd MMM yy'),
                      float(val),
                      float(capital),
                      float(interest),
                      float(inttot),
                      ]
        data.append(month_data)
        lastval = Decimal(val)
    return data
