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
	o.do_all_calcs()
	p_option = o.getPct()
	p_dol = o.getPrc()
	Delta = o.getDelta()
	Theta = o.getTheta()
	Rho = o.getRho()
	Hedge = o.getHedge()
	Gamma = o.getGamma()
	Vega = o.getVega()

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



