import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from numpy import log, exp, sqrt
from scipy.stats import norm
# import Option_Vals

rf = 0.01
rd = 0.01
t = 1/12
s0 = 100
sigma25 = 0.15
atm = 0.10
sigma75 = 0.15

vs = VolSmile(atm, sigma25, sigma75, t, s0, rd, rf)
vs.plot()
call_prices, strikes = vs.calc_option_prices()
print('The probability of spot being higher than 105 in 1 month is ' + str(vs.calc_prob(105)))
