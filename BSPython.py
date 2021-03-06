import xlwings as xw
import numpy as np
import pandas as pd
import math
from scipy import log, exp, sqrt
from scipy.stats import norm
from Option_Vals import Option_Vals

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
	o = Option_Vals(n, f, x, v, rf, rd, t, isCall)
	# o.calcIntermediates()
	#o.do_all_calcs()
	o.calc_pct()
	o.calc_prc()
	o.calc_delta()
	o.calc_gamma()
	o.calc_theta()
	o.calc_rho()
	o.calc_vega()
	o.calc_hedge()

	p_option = o.OptPct
	p_dol = o.OptPrc
	delta = o.Delta
	theta = o.Theta
	rho = o.Rho
	hedge = o.Hedge
	gamma = o.Gamma
	vega = o.Vega

	#Paste Values to spreadsheet
	wb.sheets[0].range("Opt_prc_pct").value = p_option * 100
	wb.sheets[0].range("Opt_pct_label").value = "Option Price (%)"
	wb.sheets[0].range("Opt_prc_pct").NumberFormat = "_(* #,##0.000_);_(* (#,##0.000);_(* ""-""??_);_(@_)"
	wb.sheets[0].range("Opt_prc_not").value = p_dol
	wb.sheets[0].range("Opt_not_label").value  = "Option Price"
	wb.sheets[0].range("Opt_theta").value = theta
	wb.sheets[0].range("Opt_theta").NumberFormat = "_(* #,##0.000_);_(* (#,##0.000);_(* ""-""??_);_(@_)"
	wb.sheets[0].range("Theta_label").value = "Theta"
	wb.sheets[0].range("Opt_delta").value = delta
	wb.sheets[0].range("Opt_delta").NumberFormat = "_(* #,##0.000_);_(* (#,##0.000);_(* ""-""??_);_(@_)"
	wb.sheets[0].range("Delta_label").value = "Delta"
	wb.sheets[0].range("Opt_gamma").value = gamma
	wb.sheets[0].range("Gamma_label").value = "Gamma"
	wb.sheets[0].range("Opt_rho").value = rho
	wb.sheets[0].range("Opt_rho").NumberFormat = "_(* #,##0.000_);_(* (#,##0.000);_(* ""-""??_);_(@_)"
	wb.sheets[0].range("Rho_label").value = "Rho"
	wb.sheets[0].range("Opt_vega").value = vega
	wb.sheets[0].range("Vega_label").value = "Vega"
	wb.sheets[0].range("Hedge").value = hedge
	wb.sheets[0].range("Hedge_label").value = "Hedge (USD)"



