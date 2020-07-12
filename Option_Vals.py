import numpy as np
import pandas as pd
import math
from scipy import log, exp, sqrt
from scipy.stats import norm

class Option_Vals():  
	# Inputs
	_isCall = None
	n = None
	f = None
	s0 = None
	x = None
	v = None
	rf = None
	rd = None
	t = None

	# intermediate values
	_intermediates = None

	# Outputs
	p_option = None
	p_dol = None
	d_option = None
	_theta = None
	_rho = None
	_delta = None
	_hedge = None
	_gamma = None
	_vega = None

	def __init__(self, notional, forward, strike, volatility, r_f, r_d, t, call):
		self.n = notional
		self.f = forward
		self.x = strike
		self.v = volatility
		self.rf = r_f
		self.rd = r_d
		self._isCall = call
		self.t = t
		self.s0 = forward * exp((r_f - r_d) * t)
		self._intermediates = self.calcIntermediates()

	@property
	def isCall(self):
		return self._isCall

	@isCall.setter
	def isCall(self, call):
		self._isCall = call

	@property
	def Notional(self):
		return self.n

	@Notional.setter
	def Notional(self, notional):
		self.n = notional

	@property
	def Spot(self):
		return self.s0

	@Spot.setter
	def Spot(self, spot):
		self.s0 = spot
		self._intermediates = self.calcIntermediates()

	@property
	def Forward(self):
		return self.f

	@Forward.setter
	def Forward(self, forward):
		self.f = forward

	@property
	def Strike(self):
		return self.x

	@Strike.setter
	def Strike(self, strike):
		self.x = strike
		self._intermediates = self.calcIntermediates()

	@property
	def Volatility(self):
		return self.v

	@Volatility.setter
	def Volatility(self, volatility):
		self.v = volatility
		self._intermediates = self.calcIntermediates()

	@property
	def ForeignRate(self):
		return self.rf

	@ForeignRate.setter
	def ForeignRate(self, r_f):
		self.rf = r_f
		self._intermediates = self.calcIntermediates()

	@property
	def DomesticRate(self):
		return self.rd

	@DomesticRate.setter
	def DomesticRate(self, r_d):
		self.rd = r_d
		self._intermediates = self.calcIntermediates()

	@property
	def TimeExp(self):
		return self.t

	@TimeExp.setter
	def TimeExp(self, t_exp):
		self.t= t_exp
		self._intermediates = self.calcIntermediates()
	
	@property
	def OptPct(self):
		return self.p_option

	@OptPct.setter
	def OptPct(self, p):
		self.p_option = p

	@property
	def OptPrc(self):
		return self.p_dol

	@OptPrc.setter
	def OptPrc(self, p):
		self.p_dol = p

	@property
	def Delta(self):
		return self._delta

	@Delta.setter
	def Delta(self, delta):
		self._delta = delta

	@property
	def Gamma(self):
		return self._gamma

	@Gamma.setter
	def Gamma(self, gamma):
		self._gamma = gamma

	@property
	def Theta(self):
		return self._theta

	@Theta.setter
	def Theta(self, theta):
		self._theta = theta

	@property
	def Vega(self):
		return self._vega

	@Vega.setter
	def Vega(self, vega):
		self._vega = vega

	@property
	def Rho(self):
		return self._rho

	@Rho.setter
	def Rho(self, rho):
		self._rho = rho

	@property
	def Hedge(self):
		return self._hedge

	@Hedge.setter
	def Hedge(self, hedge):
		self._hedge = hedge

	def getIntermediates(self):
		return self._intermediates

	def calcIntermediates(self):
		s0 = self.Spot
		x = self.Strike
		v = self.Volatility
		rf = self.ForeignRate
		rd = self.DomesticRate
		t = self.TimeExp

    	#Calculate intermediate values
		d1 = (log(s0 / x) + t * (rd - rf + pow(v, 2) / 2)) / (v * sqrt(t))
		d2 = d1 - v * sqrt(t)
		N_d1 = norm.cdf(d1)
		N_minusd1 = norm.cdf(-d1)
		N_d2 = norm.cdf(d2)
		N_minusd2 = norm.cdf(-d2)
		N_prime_d1 = (1.0 / sqrt(2 * math.pi) * exp((-d1**2) / 2))
		self.Forward = s0 * exp((rd - rf) * t)

		opt = dict()
		opt["d1"] = d1
		opt["d2"] = d2
		opt["N_d1"] = N_d1
		opt["N_minusd1"] = N_minusd1
		opt["N_d2"] = N_d2
		opt["N_minusd2"] = N_minusd2
		opt["N_prime_d1"] = N_prime_d1
		return opt


	def calc_pct(self):
		s0 = self.Spot
		f = self.Forward
		x = self.Strike
		rd = self.DomesticRate
		t = self.TimeExp
		opt_isCall = self.isCall
		o = self.getIntermediates()

		if opt_isCall:
			p = (exp(-rd * t) * (f * o["N_d1"] - x * o["N_d2"])) / s0
		else:
			p = (exp(-rd * t) * (x * o["N_minusd2"] - f * o["N_minusd1"])) / s0
		self.OptPct  = p

	def calc_prc(self):
		self.OptPrc = self.Notional * self.OptPct
		
	def calc_delta(self, isMktConvention = True):
		o = self.getIntermediates()
		rf = self.ForeignRate
		t = self.TimeExp
		opt_isCall = self.isCall

		if opt_isCall:
			self.Delta = exp(-rf * t) * o["N_d1"]
		else:
			self.Delta = exp(-rf * t) * (o["N_d1"] - 1)

		if isMktConvention:
			self.Delta = self.Delta - self.OptPct


	def calc_theta(self):
		s0 = self.Spot
		x = self.Strike
		v = self.Volatility
		rf = self.ForeignRate
		rd = self.DomesticRate
		t = self.TimeExp
		opt_isCall = self.isCall
		o = self.getIntermediates()

		if opt_isCall:
			self.Theta = (-s0 * o["N_prime_d1"] * v * exp(-rf * t) / (2 * sqrt(t)) + rf * s0 * o["N_d1"] * exp(-rf * t) - rd * x * exp(-rd * t) * o["N_d2"]) / 100
		else:
			self.Theta = (-s0 * o["N_prime_d1"] * v * exp(-rf * t) / (2 * sqrt(t)) - rf * s0 * o["N_minusd1"] * exp(-rf * t) + rd * x * exp(-rd * t) * o["N_minusd2"]) / 100

	def calc_rho(self):
		x = self.Strike
		rd = self.DomesticRate
		t = self.TimeExp
		opt_isCall = self.isCall
		o = self.getIntermediates()

		if opt_isCall:
			self.Rho = x * t * exp(-rd * t) * o["N_d2"] / 100
		else:
			self.Rho = -x * t * exp(-rd * t) * o["N_minusd2"] / 100


	def calc_gamma(self, isMktConvention = True):
		o = self.getIntermediates()
		self.Gamma = self.Notional * o["N_prime_d1"] * exp(-self.ForeignRate * self.TimeExp) / (self.Spot * self.Volatility * sqrt(self.TimeExp))
		if isMktConvention:
			self.Gamma = self.Gamma * self.Spot / 100

	def calc_vega(self,isMktConvention = True):
		o = self.getIntermediates()
		self.Vega = 100 * self.Spot * sqrt(self.TimeExp) * o["N_prime_d1"] * exp(-self.ForeignRate * self.TimeExp)
		if isMktConvention:
			oldOptPrc = self.OptPct
			oldVol = self.Volatility
			self.Volatility = oldVol + 0.01
			self.calc_pct()
			newOptPrc = self.OptPct
			self.Volatility = oldVol
			self.OptPct = oldOptPrc
			self.Vega = self.Notional * (newOptPrc- oldOptPrc)

	def calc_hedge(self):
		self.Hedge = -self.Notional * self.Delta


	# def Get_OptionItems_BS_Theoretical(self):
	# 	o = self.getIntermediates()

    
 #    	# Calculate Greeks (formulas do not depend on option type)

	# 	self.calc_gamma(False)
	# 	self.calc_vega(False)
	# 	self.calc_delta(False)
	# 	self.calc_theta()
	# 	self.calc_rho()
	# 	self.calc_pct()
	# 	self.calc_prc()
	# 	self.calc_hedge(False)
    
 #    	# Calculate option value and Greeks

	# 	opt = dict()
	# 	opt["opt_price"] = self.OptPct
	# 	opt["opt_dol"] = self.OptPrc
	# 	opt["delta"] = self.Delta
	# 	opt["gamma"] = self.Gamma
	# 	opt["rho"] = self.Rho
	# 	opt["vega"] = self.Vega
	# 	opt["theta"] = self.Theta
	# 	return opt



	# def do_all_calcs(self):

 #    	# Do all calculations
	# 	o = self.Get_OptionItems_BS_Theoretical()
	# 	oldSpot = self.Spot
	# 	self.Spot = oldSpot/0.99
	# 	o_new_spot = self.Get_OptionItems_BS_Theoretical()
	# 	self.Spot = oldSpot
	# 	oldVol = self.Volatility
	# 	self.Volatility = oldVol + 0.01
	# 	o_new_vol = self.Get_OptionItems_BS_Theoretical()
	# 	self.Volatility = oldVol
	# 	self.OptPct = o["opt_price"]
	# 	self.OptPrc = o["opt_dol"]
	# 	d_option = o["delta"]
	# 	self.Theta = o["theta"]
	# 	self.Rho = o["rho"]
	# 	self.Delta = d_option - self.OptPct
	# 	self.Hedge = -self.Notional * self.Delta
	# 	d_option_new = o_new_spot["delta"]
	# 	self.Gamma = o["gamma"] * self.Spot / 100
	# 	p_option_new = o_new_vol["opt_price"]
	# 	self.Vega = self.Notional * (p_option_new - self.OptPct)
