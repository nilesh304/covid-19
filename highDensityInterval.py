import pandas as pd
import numpy as np


posteriors = pd.read_csv("posterior.csv")
print(posteriors.columns)
def highest_density_interval(pmf, p=.9, debug=False):
    print(pmf.describe())
    print("hello")
    # If we pass a DataFrame, just call this recursively on the columns
    if(isinstance(pmf, pd.DataFrame)):
        return pd.DataFrame([highest_density_interval(pmf[col], p=p) for col in pmf],index=pmf.columns)
    
    cumsum = np.cumsum(pmf.values)
    
    # N x N matrix of total probability mass for each low, high
    total_p = cumsum - cumsum[:, None]
    
    # Return all indices with total_p > p
    lows, highs = (total_p > p).nonzero()
    
    # Find the smallest range (highest density)
#     print("total_p\n{}lows\n{}highs\n{}".format(total_p,lows,highs))
#     print("\nhighs and lows: ",len(highs),len(lows))
    
#     print(total_p.max())
    if len(lows)>0:
        best = (highs - lows).argmin()

        low = pmf.index[lows[best]]
        high = pmf.index[highs[best]]
    
        return pd.Series([low, high],
                         index=[f'Low_{p*100:.0f}',
                                f'High_{p*100:.0f}'])
    

# hdi = highest_density_interval(posteriors, debug=True)
# hdi.tail()