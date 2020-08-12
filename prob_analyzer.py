s0 = 6.328 
x50 =[6.34, 6.35, 6.36, 6.38, 6.41] 
x25 = [6.37, 6.39, 6.41, 6.47, 6.58] 
x75 = [6.32, 6.32, 6.32, 6.31, 6.30] 
rd = [0.0313, 0.0263, 0.0235, 0.0207, 0.0183] 
rf = [0.0044, 0.0045, 0.0046, 0.005, 0.0055] 
tenors = [1.0/12, 1.0/6, 1.0/4, 1.0/2, 1] 
v25 = [0.024, 0.025, 0.023, 0.0305, 0.0385]
v75 = [0.018, 0.0185, 0.016, 0.0215, 0.0255]
atm = [0.02, 0.0205, 0.021, 0.024, 0.029]
probs = np.zeros((25,5))


def get_zero_prob_index(vs, spot):
	increment = spot * 0.001
	upper = spot + increment
	lower = spot - increment
	notFound = True 
	while notFound:
		p_lower = 1 - vs.calc_prob(lower)
		p_upper = vs.calc_prob(upper)
		if p_lower <= 0.005 or p_upper <= 0.005:
			notFound = False
		else:
			upper = upper + increment
			lower = lower - increment
	return lower

def calc_vol(strike, delta, t, rd, rf, s0):
    # This uses the inverse normal distribution

    a = t/2.0
    b = -norm.ppf(delta*exp(rd * t)) * sqrt(t)
    c = log(s0/strike) + (rd - rf) * t

    x = (-b + sqrt((b**2) - (4*a*c)))/(2 * a)

    return x

    
# def populate_delta_vols_from_delta_strikes():
#     for idx_tenor in range(0,5):
#         v25[idx_tenor] = calc_vol(x25[idx_tenor], 0.25, tenors[idx_tenor], rd[idx_tenor], rf[idx_tenor], s0)
#         v75[idx_tenor] = calc_vol(x75[idx_tenor], 0.75, tenors[idx_tenor], rd[idx_tenor], rf[idx_tenor], s0)
#         atm[idx_tenor] = calc_vol(x50[idx_tenor], 0.5, tenors[idx_tenor], rd[idx_tenor], rf[idx_tenor], s0)

        
# populate_delta_vols_from_delta_strikes()   
vs = VolSmile(atm[4], v25[4], v75[4], tenors[4], s0, rd[4], rf[4])
sLower = get_zero_prob_index(vs, s0)
sUpper = s0 + (s0 - sLower)
spots = np.linspace(sLower, sUpper, 25)

for i in range (0,len(tenors)):
    for j in range (0,len(spots)):
        vs = VolSmile(atm[i], v25[i], v75[i], tenors[i], s0, rd[i], rf[i])
        probs[j][i] = vs.calc_prob(spots[j])
        print(vs.calc_prob(spots[j]))
            
rounded_spots = np.round(spots,2)
rounded_spots = rounded_spots[::-1]
prob_df = pd.DataFrame(probs, columns= ['01M','02M','03M','06M','12M'], index=rounded_spots)
print("USD/CNY Probability Analyzer", prob_df, sep='\n')
