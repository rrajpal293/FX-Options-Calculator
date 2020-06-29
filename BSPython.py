import xlwings as xw
import numpy as np
import pandas as pd
import math
from scipy import log, exp, sqrt
from scipy.stats import norm

class Option_Vals():  
    opt_price = None
    opt_dol = None
    Delta = None
    Gamma = None
    Rho = None
    Vega = None
    Theta = None

def hello_xlwings():
    wb = xw.Book.caller()
    wb.sheets[0].range("A1").value = "Hello xlwings!"


def calc_avg():
	wb = xw.Book.caller()
	x1 = wb.sheets[0].range("B4").value
	x2 = wb.sheets[0].range("B5").value
	x3 = wb.sheets[0].range("B6").value
	x4 = wb.sheets[0].range("B7").value
	rng = wb.sheets[0].range("B4:B7").value
	wb.sheets[0].range("E24").value = np.mean(rng)

def do_all_calcs():
	isCall = False

    # Read the inputs
	wb = xw.Book.caller()
	n = wb.sheets[0].range("Notional").value
	x = wb.sheets[0].range("Strike_Price").value
	f = wb.sheets[0].range("Forward_Rate").value
	v = wb.sheets[0].range("Volatility").value
	rf = wb.sheets[0].range("r_f").value
	rd = wb.sheets[0].range("r_d").value
	t = wb.sheets[0].range("t_exp").value
	s0 = f * exp((rf - rd) * t)
	if (wb.sheets[0].range("TypeOfOption").value == 1):
		isCall = True
    
    # Do all calculations
    
	o = Get_OptionItems_Theoretical(n, s0, x, v, rf, rd, t, isCall)
	o_new_spot = Get_OptionItems_Theoretical(n, s0 / 0.99, x, v, rf, rd, t, isCall)
	o_new_vol = Get_OptionItems_Theoretical(n, s0, x, v + 0.01, rf, rd, t, isCall)
	p_option = o.opt_price
	p_dol = n * p_option
	d_option = o.Delta
	Theta = o.Theta
	Rho = o.Rho
	Delta = d_option - p_option
	Hedge = -n * Delta
	d_option_new = o_new_spot.Delta
	Gamma = o.Gamma * s0 / 100
	p_option_new = o_new_vol.opt_price
	Vega = n * (p_option_new - p_option)

	#Paste Values to spreadsheet
	wb.sheets[0].range("Opt_prc_pct").value = p_option * 100
	wb.sheets[0].range("Opt_pct_label").value = "Option Price (%)"
	wb.sheets[0].range("Opt_prc_pct").NumberFormat = "_(* #,##0.000_);_(* (#,##0.000);_(* ""-""??_);_(@_)"
	wb.sheets[0].range("Opt_prc_not").value = p_dol
	wb.sheets[0].range("Opt_not_label").value  = "Option Price"
	wb.sheets[0].range("Opt_theta").value = Theta
	wb.sheets[0].range("Opt_theta").NumberFormat = "_(* #,##0.000_);_(* (#,##0.000);_(* ""-""??_);_(@_)"
	wb.sheets[0].range("Theta_label").value = "Theta"
	wb.sheets[0].range("Opt_delta").value = Delta
	wb.sheets[0].range("Opt_delta").NumberFormat = "_(* #,##0.000_);_(* (#,##0.000);_(* ""-""??_);_(@_)"
	wb.sheets[0].range("Delta_label").value = "Delta"
	wb.sheets[0].range("Opt_gamma").value = Gamma
	wb.sheets[0].range("Gamma_label").value = "Gamma"
	wb.sheets[0].range("Opt_rho").value = Rho
	wb.sheets[0].range("Opt_rho").NumberFormat = "_(* #,##0.000_);_(* (#,##0.000);_(* ""-""??_);_(@_)"
	wb.sheets[0].range("Rho_label").value = "Rho"
	wb.sheets[0].range("Opt_vega").value = Vega
	wb.sheets[0].range("Vega_label").value = "Vega"
	wb.sheets[0].range("Hedge").value = Hedge
	wb.sheets[0].range("Hedge_label").value = "Hedge (USD)"

def Get_OptionItems_Theoretical(n, s0, x, v, rf, rd, t, isCall):

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

    p_dol = n * p / 100

    opt = Option_Vals()
    opt.opt_price = p
    opt.opt_dol = p_dol
    opt.Delta = Delta
    opt.Gamma = Gamma
    opt.Rho = Rho
    opt.Vega = Vega
    opt.Theta = Theta
    
    return opt
