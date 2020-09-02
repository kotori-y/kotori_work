# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 08:23:02 2020

@Author: Zhi-Jiang Yang, Dong-Sheng Cao
@Institution: CBDD Group, Xiangya School of Pharmaceutical Science, CSU, China
@Homepage: http://www.scbdd.com
@Mail: yzjkid9@gmail.com; oriental-cds@163.com
@Blog: https://blog.iamkotori.com

♥I love Princess Zelda forever♥
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import relfreq
from scipy.interpolate import spline
# from scipy.interpolate import interp1d
import warnings
warnings.filterwarnings("ignore")

def transColor(color):
    return tuple((x/255 for x in color))

def drawFrequency(data, numBins=10, ax=None, **kwargs):
    
    if not ax:
        f, ax = plt.subplots(figsize=(8, 4.5))
    else:
        pass
    
    data = data.flatten()
    res = relfreq(data, numbins=numBins)
    
    y = res.frequency
    X = res.lowerlimit + np.linspace(
        0, res.binsize*y.size, y.size
        )
    
    station = X.copy()
    X = np.linspace(X.min(), X.max(), 800)
    y = spline(station, y, X)
    
    ax.plot(X, y, **kwargs)
    
    
    try:
        return f
    except Exception:
        return None
    
    
    
if "__main__" == __name__:
    colors = [(90, 138, 198),
              (248, 105, 107),]
    f, ax = plt.subplots(figsize=(8, 8*0.618))
    
    data = {
        256: np.random.randn(256,1024),
        512: np.random.randn(512,1024)
        }
    
    for key, color in zip(data.keys(), colors):
        drawFrequency(
            data[key], numBins=80, ax=ax, 
            color=transColor(color),
            lw=2.5,
            label=key,
            alpha=0.9
            )
    
    ax.spines["bottom"].set_linewidth(1.8)
    ax.spines["left"].set_linewidth(1.8)
    ax.spines["top"].set_linewidth(1.8)
    ax.spines["right"].set_linewidth(1.8)
    
    ax.spines["bottom"].set_color("#93949a")
    ax.spines["left"].set_color("#93949a")
    ax.spines["right"].set_color("#93949a")
    ax.spines["top"].set_color("#93949a")
    
    ax.tick_params(direction="in", which="both", length=5, color="#93949a")
    
    ax.set_xlabel("$X_{label}$",
                  fontdict={
                      "family": "Calibri", 
                      "size": 16,
                      "weight":"bold",
                      })
    
    ax.set_ylabel("Frequent",
                  fontdict={
                      "family": "Calibri", 
                      "size":16,
                      "weight":"bold",
                      })
    
    # ax.set_xlim([-1, 1])
    # ax.set_ylim(-0.001)
    ax.grid(ls='--')
    
    legend_properties = {"weight":"bold", 
                         "family": "Calibri",
                         "size":14}

    plt.legend(prop=legend_properties)
        
        