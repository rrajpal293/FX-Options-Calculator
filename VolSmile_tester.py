import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from numpy import log, exp, sqrt
from scipy.stats import norm

rf = 0.00073
rd = -0.00357
t = 31/365
s0 = 105.92
sigma25 = 0.0665
atm = 0.0639
sigma75 = 0.0739

vs = VolSmile(atm, sigma25, sigma75, t, s0, rd, rf)
vs.plot()
call_prices, strikes = vs.calc_option_prices()
print('The probability of spot being higher than 105 in 1 month is ' + str(vs.calc_prob(105)))
