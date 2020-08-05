import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from numpy import log, exp, sqrt
from scipy.stats import norm
from Option_Vals import Option_Vals

class VolSmile():  

    # inputs
    _atm = None
    _rr25 = None
    _bfly25 = None
    _s0 = None
    _f = None
    _t = None
    _rd = None
    _rf = None


    #outputs
    _vol15 = None
    _vol25 = None
    _vol75 = None
    _vol85 = None


    def __init__(self, atm, sigma25, sigma75, t, s0, rd, rf):
        self._atm = atm
        self._vol25 = sigma25
        self._vol75 = sigma75
        self._t = t
        self._s0 = s0
        self._rd = rd
        self._rf = rf
        self._f = s0 * exp(-(rf - rd) * t)
        self._rr25 = sigma25 - sigma75;
        self._bfly25 = 0.5 * (sigma25 + sigma75) - atm


    def calcVols(self):
        self._vol25 = self._atm + 0.5 * self._rr25 + self._bfly25
        self._vol75 = self._atm - 0.5 * self._rr25 + self._bfly25
        self._vol15 = self.malz_quadratic(0.15)
        self._vol85 = self.malz_quadratic(0.85)

    def malz_quadratic(self, input_delta):

        return self._atm - 2 * self._rr25 * (input_delta - 0.5) + 16 * self._bfly25 * (input_delta - 0.5)**2


    def calc_strike(self, sigma, delta):
        # This uses the Newton Raphson method

        x = s0 * exp(sigma * self._t * norm.ppf(delta) - (self._rd - self._rf + (sigma**2)/self._t) * self._t)
        return x

    def calc_option_prices(self):
        # This uses the Newton Raphson method
        isCall = True
        deltas= np.linspace(0.01, 1, 100);
        strikes = [0] * 100; #initialize mnatrix of zeros
        vols = [0] * 100; # initialize matrix of zeros
        call_prices = [0] * 100
        for i in range(0, 100):
            vols[i] = self.malz_quadratic(deltas[i])
        for i in range(0, 100):
            strikes[i] = self.calc_strike(vols[i], deltas[i])
            o = Option_Vals(1000000, self._f, strikes[i], vols[i], self._rf, self._rd, self._t, isCall)
            o.calc_pct()
            call_prices[i] = o.OptPct

        return call_prices, strikes

    def plot(self):

        fig, ax = plt.subplots()
        deltas= np.linspace(0.01, 1, 100);
        strikes = [0] * 100; #initialize mnatrix of zeros
        vols = [0] * 100; # initialize matrix of zeros
        for i in range(0, 100):
            vols[i] = self.malz_quadratic(deltas[i])
        for i in range(0, 100):
            strikes[i] = self.calc_strike(vols[i], deltas[i])

        ax.scatter(strikes, vols)
        ax.set_xlabel('Strike', fontsize=15)
        ax.set_ylabel('Volatility', fontsize=15)
        ax.set_title('Volatility Smile')
        ax.grid(True)

        fig.tight_layout()

        plt.show()


    def newtons_method(f, df, x, e, max_iter):
        dist = abs(f(x))
        it = 0
        while dist > e and it < max_iter:
            x = x - f(x)/df(x)
            dist = abs(f(x))
            it = it + 1
        return x