import numpy as np
import pandas as pd
import math
from scipy import log, exp, sqrt
from scipy.stats import norm

class Option_Vals():  
	# Inputs
	n = None
	f = None
	s0 = None
	x = None
	v = None
	rf = None
	rd = None
	t = None
	isCall = None

	# Outputs
	p_option = None
	p_dol = None
	d_option = None
	Theta = None
	Rho = None
	Delta = None
	Hedge = None
	Gamma = None
	Vega = None

	def __init__(self, notional, forward, strike, volatility, r_f, r_d, t, isCall):
		self.n = notional
		self.f = forward
		self.x = strike
		self.v = volatility
		self.rf = r_f
		self.rd = r_d
		self.isCall = isCall
		self.t = t
		self.s0 = forward * exp((r_f - r_d) * t)

	def setNotional(self, notional):
		self.n = notional

	def setSpot(self, forward):
		self.f = forward

	def setStrike(self, strike):
		self.x = strike

	def setVolatility(self, volatility):
		self.v = volatility

	def setForeignRate(self, r_f):
		self.rf = r_f

	def setDomesticRate(self, r_d):
		self.rd = r_d

	def setTimeExp(self, t_exp):
		self.t= t_exp

	def getPct(self):
		return self.p_option

	def getPrc(self):
		return self.p_dol

	def getDelta(self):
		return self.Delta

	def getGamma(self):
		return self.Gamma

	def getTheta(self):
		return self.Theta

	def getVega(self):
		return self.Vega

	def getRho(self):
		return self.Rho

	def getHedge(self):
		return self.Hedge

	def Get_OptionItems_BS_Theoretical(self, n, s0, x, v, rf,rd,t, isCall):
    	#Calculate intermediate values
		d1 = (log(s0 / x) + t * (rd - rf + pow(v, 2) / 2)) / (v * sqrt(t))
		d2 = d1 - v * sqrt(t)
		N_d1 = norm.cdf(d1)
		N_minusd1 = norm.cdf(-d1)
		N_d2 = norm.cdf(d2)
		N_minusd2 = norm.cdf(-d2)
		N_prime_d1 = (1.0 / sqrt(2 * math.pi) * exp((-d1**2) / 2))
		f = s0 * exp((rd - rf) * t)
    
    	#Calculate Greeks (formulas do not depend on option type)
		Gamma = n * N_prime_d1 * exp(-rf * t) / (s0 * v * sqrt(t))
		Vega = 100 * s0 * sqrt(t) * N_prime_d1 * exp(-rf * t)
    
    	#Calculate option value and Greeks
		if isCall:
			Delta = exp(-rf * t) * N_d1
			Theta = (-s0 * N_prime_d1 * v * exp(-rf * t) / (2 * sqrt(t)) + rf * s0 * N_d1 * exp(-rf * t) - rd * x * exp(-rd * t) * N_d2) / 100
			Rho = x * t * exp(-rd * t) * N_d2 / 100
			p = (exp(-rd * t) * (f * N_d1 - x * N_d2)) / s0
		else:
			Delta = exp(-rf * t) * (N_d1 - 1)
			Theta = (-s0 * N_prime_d1 * v * exp(-rf * t) / (2 * sqrt(t)) - rf * s0 * N_minusd1 * exp(-rf * t) + rd * x * exp(-rd * t) * N_minusd2) / 100
			Rho = -x * t * exp(-rd * t) * N_minusd2 / 100
			p = (exp(-rd * t) * (x * N_minusd2 - f * N_minusd1)) / s0

		p_dol = n * p

		opt = dict()
		opt["opt_price"] = p
		opt["opt_dol"] = p_dol
		opt["delta"] = Delta
		opt["gamma"] = Gamma
		opt["rho"] = Rho
		opt["vega"] = Vega
		opt["theta"] = Theta
		return opt

	def do_all_calcs(self):

    	# Do all calculations
		o = self.Get_OptionItems_BS_Theoretical(self.n, self.s0, self.x, self.v, self.rf, self.rd, self.t, self.isCall)
		o_new_spot = self.Get_OptionItems_BS_Theoretical(self.n, self.s0 / 0.99, self.x, self.v, self.rf, self.rd, self.t, self.isCall)
		o_new_vol = self.Get_OptionItems_BS_Theoretical(self.n, self.s0, self.x, self.v + 0.01, self.rf, self.rd, self.t, self.isCall)
		self.p_option = o["opt_price"]
		self.p_dol = o["opt_dol"]
		self.d_option = o["delta"]
		self.Theta = o["theta"]
		self.Rho = o["rho"]
		self.Delta = self.d_option - self.p_option
		self.Hedge = -self.n * self.Delta
		d_option_new = o_new_spot["delta"]
		self.Gamma = o["gamma"] * self.s0 / 100
		p_option_new = o_new_vol["opt_price"]
		self.Vega = self.n * (p_option_new - self.p_option)
