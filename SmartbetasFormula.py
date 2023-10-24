#Formeln für die statistische Auswertung

   
#Annualisierte Rendite    
def annualize_rets(r):
    
    compounded_growth = (1+r).prod()
    n_periods = r.shape[0]
    return compounded_growth**(12/n_periods)-1




#Volatility   
def vol(r):
    
    "Nimmt monatliche Rendite für 6 Portfolios und gibt standard deviation hoch zwei (Variance) zurück"
    r.std()**2
    



#Annualisierte Volatilität
def annualize_vol(r):
    
    return r.std()*(12**0.5)
    
    
    
#Skewness
def skewness(r):
    
    """
    Alternative zu scipy.stats.skew()    
    Berechnet die Skewness der angegebenen Serie oder des Dataframe
    Gibt einen Float oder eine Serie zurück
    """
    
    demeaned_r = r - r.mean()
    #Use the population standard deviation (not n-1), so set dof=0
    sigma_r = r.std(ddof = 0)
    exp = (demeaned_r**3).mean()
    return exp/sigma_r**3
    
#Kurtotis
def kurtosis(r):
    
    """
    Alternative to scipy.stats.kurtosis()
    Computes the kurtosis of the supplied Series or Dataframe
    Returns a float or series
    """
    demeaned_r = r - r.mean()
    # use the population standard deviation, so set dof=0
    sigma_r = r.std()
    exp = (demeaned_r**4).mean()
    return exp/sigma_r**4

    
#VaR-Cornisch Fisher 
from scipy.stats import norm    
def var_gaussian(r, level=5):
    """
    Returns the Parametric  
    """
    # compute the Z score assuming it was Gaussian
    z = norm.ppf(level/100)
    s = skewness(r)
    k = kurtosis(r)
    z = (z +
            (z**2 - 1)*s/6 +
            (z**3 -3*z)*(k-3)/24 -
            (2*z**3 - 5*z)*(s**2)/36
        )
    return -(r.mean() + z*r.std(ddof=0))
    

    
#Normalität
import scipy.stats
def is_normal(r,level = 0.05):
    #Konfidenzniveau von 5%
    """
    Impelmentiert Jarque-Bera test, um zu wissen, ob die Series normal ist oder nicht.
    Gibt True, wenn es die Normalitität gibt.
    
    """
    
    statistic, p_value = scipy.stats.jarque_bera(r)
    return p_value > level
    

        
    
    
    
#Sharp ratio mit konstant Risikofreien Rate   
def sharpe_ratio(r):
    """
    Berechnet die annualisierte Sharpe Ratio einer Reihe(set) von Renditen
    
    Risikofreien Rate 0.03
    """
    
    excess_ret = r - 0.03
    ann_ex_ret = annualize_rets(excess_ret)
    ann_vol = annualize_vol(r)
    return ann_ex_ret/ann_vol


#Sharp ratio mit reale Risikofreien Rate 0.012141176470588242 (Entwickelte Märkte Risiko frei Rate 2004 - 2020) 
def sharpe_ratio_r(r):

    """
    Berechnet die annualisierte Sharpe Ratio einer Reihe(set) von Renditen
    
    Dieses Mal mit mit reale Risikofreien Rate 0.012 (Entwickelte Märkte Risiko frei Rate 2004 - 2020) 
    
    """
    
    excess_ret = r - 0.012141176470588242
    ann_ex_ret = annualize_rets(excess_ret)
    ann_vol = annualize_vol(r)
    return ann_ex_ret/ann_vol


import pandas as pd
def drawdown(return_series):
    """
    Nimmt eine Zeitreihe (Time Series) von Renditen
    berechnet und liefert einen Datenframe, der Folgendes enthält:
    The wealth index
    The previous peaks
    percent drawdowns
    
    """
    
    wealth_index = 1000*(1+return_series).cumprod()
    previous_peaks = wealth_index.cummax()
    drawdowns = (wealth_index - previous_peaks)/previous_peaks
    
    return pd.DataFrame({"wealth" : wealth_index,
                         "Peaks" : previous_peaks,
                         "Drawdown" : drawdowns})

    

#Kumulierte Rendite
def calculate_cumulative_return(r):
    
    "Nimmt monatliche Rendite für 6 Portfolios und gibt Cumulative returns zurück, danach kann man auch jährlich machen"
    
    cumulative_return = 1.0
    for return_value in r:
        cumulative_return *= (1 + return_value)
    return cumulative_return



    