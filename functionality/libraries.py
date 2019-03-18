# Standard Libaries Script 

from __future__ import division
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
from glob import glob
import pdb
from ipykernel import kernelapp as app
import itertools as it

#from sklearn.cross_validation import train_test_split
from sklearn import metrics

from sklearn.metrics import accuracy_score, log_loss
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
import sklearn

### Extra Libraries




# Settings 
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
seed = 7
np.random.seed(seed)

import warnings
warnings.filterwarnings('ignore')



from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler

def Normalisation(low,high,df):
    listed = list(df)
    scaler = MinMaxScaler(feature_range=(low,high))
    scaled = scaler.fit_transform(df)
    df = pd.DataFrame(scaled)
    df.columns = listed
    return df


#from tsfresh import extract_relevant_features
#from tsfresh import extract_features

import numpy as np
from scipy import stats


import plotly.plotly as py
import pandas as pd

import plotly 
plotly.tools.set_credentials_file(username='xxxxxx', api_key='xxxxxx')

from sklearn.model_selection import TimeSeriesSplit
from sklearn.cross_validation import cross_val_score


from scikitplot import plotters as skplt


from scikitplot import plotters as skplt # more flexible import 
import matplotlib.pyplot as plt

from sklearn.metrics import classification_report

import seaborn as sns



import random 
def warn(*args, **kwargs): pass

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler

from sklearn.model_selection import train_test_split



class Columns(object):
    OPEN='open'
    HIGH='high'
    LOW='low'
    CLOSE='close'
    VOLUME='volume'

# def get(df, col):
#    return(df[col])

# df['close'] => get(df, COL.CLOSE)

# price=COL.CLOSE

indicators=["MA", "EMA", "MOM", "ROC", "ATR", "BBANDS", "PPSR", "STOK", "STO",
    "TRIX", "ADX", "MACD", "MassI", "Vortex", "KST", "RSI", "TSI", "ACCDIST",
    "Chaikin", "MFI", "OBV", "FORCE", "EOM", "CCI", "COPP", "KELCH", "ULTOSC",
    "DONCH", "STDDEV"]


class Settings(object):
    join=True
    col=Columns()

SETTINGS=Settings()


def out(settings, df, result):
    if not settings.join:
        return result
    else:
        df=df.join(result)
        return df


def MA(df, n, price='close'):
    """
    Moving Average
    """
    name='MA_{n}'.format(n=n)
    result = pd.Series(pd.rolling_mean(df[price], n), name=name)
    return out(SETTINGS, df, result)


def EMA(df, n, price='close'):
    """
    Exponential Moving Average
    """
    result=pd.Series(pd.ewma(df[price], span=n, min_periods=n - 1), name='EMA_' + str(n))
    return out(SETTINGS, df, result)


def MOM(df, n, price='close'):
    """
    Momentum
    """
    result=pd.Series(df[price].diff(n), name='Momentum_' + str(n))
    return out(SETTINGS, df, result)


def ROC(df, n, price='close'):
    """
    Rate of Change
    """
    M = df[price].diff(n - 1)
    N = df[price].shift(n - 1)
    result = pd.Series(M / N, name='ROC_' + str(n))
    return out(SETTINGS, df, result)


def ATR(df, n):
    """
    Average True Range
    """
    i = 0
    TR_l = [0]
    while i < len(df) - 1:  # df.index[-1]:
    # for i, idx in enumerate(df.index)
        # TR=max(df.get_value(i + 1, 'high'), df.get_value(i, 'close')) - min(df.get_value(i + 1, 'low'), df.get_value(i, 'close'))
        TR = max(df['high'].iloc[i + 1], df['close'].iloc[i] - min(df['low'].iloc[i + 1], df['close'].iloc[i]))
        TR_l.append(TR)
        i = i + 1
    TR_s = pd.Series(TR_l)
    result = pd.Series(pd.ewma(TR_s, span=n, min_periods=n), name='ATR_' + str(n))
    return out(SETTINGS, df, result)


def BBANDS(df, n, price='close'):
    """
    Bollinger Bands
    """
    MA = pd.Series(pd.rolling_mean(df[price], n))
    MSD = pd.Series(pd.rolling_std(df[price], n))
    b1 = 4 * MSD / MA
    B1 = pd.Series(b1, name='BollingerB_' + str(n))
    b2 = (df[price] - MA + 2 * MSD) / (4 * MSD)
    B2 = pd.Series(b2, name='Bollinger%b_' + str(n))
    result = pd.DataFrame([B1, B2]).transpose()
    return out(SETTINGS, df, result)


def PPSR(df):
    """
    Pivot Points, Supports and Resistances
    """
    PP = pd.Series((df['high'] + df['low'] + df['close']) / 3)
    R1 = pd.Series(2 * PP - df['low'])
    S1 = pd.Series(2 * PP - df['high'])
    R2 = pd.Series(PP + df['high'] - df['low'])
    S2 = pd.Series(PP - df['high'] + df['low'])
    R3 = pd.Series(df['high'] + 2 * (PP - df['low']))
    S3 = pd.Series(df['low'] - 2 * (df['high'] - PP))
    result = pd.DataFrame([PP, R1, S1, R2, S2, R3, S3]).transpose()
    return out(SETTINGS, df, result)


def STOK(df):
    """
    Stochastic oscillator %K
    """
    result = pd.Series((df['close'] - df['low']) / (df['high'] - df['low']), name='SO%k')
    return out(SETTINGS, df, result)


def STO(df, n):
    """
    Stochastic oscillator %D
    """
    SOk = pd.Series((df['close'] - df['low']) / (df['high'] - df['low']), name='SO%k')
    result = pd.Series(pd.ewma(SOk, span=n, min_periods=n - 1), name='SO%d_' + str(n))
    return out(SETTINGS, df, result)


def SMA(df, timeperiod, key='close'):
    result = pd.rolling_mean(df[key], timeperiod, min_periods=timeperiod)
    return out(SETTINGS, df, result)


def TRIX(df, n):
    """
    Trix
    """
    EX1 = pd.ewma(df['close'], span=n, min_periods=n - 1)
    EX2 = pd.ewma(EX1, span=n, min_periods=n - 1)
    EX3 = pd.ewma(EX2, span=n, min_periods=n - 1)
    i = 0
    ROC_l = [0]
    while i + 1 <= len(df) - 1:  # df.index[-1]:
        ROC = (EX3[i + 1] - EX3[i]) / EX3[i]
        ROC_l.append(ROC)
        i = i + 1
    result = pd.Series(ROC_l, name='Trix_' + str(n))
    return out(SETTINGS, df, result)


def ADX(df, n, n_ADX):
    """
    Average Directional Movement Index
    """
    i = 0
    UpI = []
    DoI = []
    while i + 1 <= len(df) - 1:  # df.index[-1]:
        UpMove = df.get_value(i + 1, 'high') - df.get_value(i, 'high')
        DoMove = df.get_value(i, 'low') - df.get_value(i + 1, 'low')
        if UpMove > DoMove and UpMove > 0:
            UpD = UpMove
        else:
            UpD = 0
        UpI.append(UpD)
        if DoMove > UpMove and DoMove > 0:
            DoD = DoMove
        else:
            DoD = 0
        DoI.append(DoD)
        i = i + 1
    i = 0
    TR_l = [0]
    while i < len(df) - 1:  # df.index[-1]:
        TR = max(df.get_value(i + 1, 'high'), df.get_value(i, 'close')) - min(df.get_value(i + 1, 'low'), df.get_value(i, 'close'))
        TR_l.append(TR)
        i = i + 1
    TR_s = pd.Series(TR_l)
    ATR = pd.Series(pd.ewma(TR_s, span=n, min_periods=n))
    UpI = pd.Series(UpI)
    DoI = pd.Series(DoI)
    PosDI = pd.Series(pd.ewma(UpI, span=n, min_periods=n - 1) / ATR)
    NegDI = pd.Series(pd.ewma(DoI, span=n, min_periods=n - 1) / ATR)
    result = pd.Series(pd.ewma(abs(PosDI - NegDI) / (PosDI + NegDI), span=n_ADX, min_periods=n_ADX - 1), name='ADX_' + str(n) + '_' + str(n_ADX))
    return out(SETTINGS, df, result)


def MACD(df, n_fast, n_slow, price='close'):
    """
    MACD, MACD Signal and MACD difference
    """
    EMAfast = pd.Series(pd.ewma(df[price], span=n_fast, min_periods=n_slow - 1))
    EMAslow = pd.Series(pd.ewma(df[price], span=n_slow, min_periods=n_slow - 1))
    MACD = pd.Series(EMAfast - EMAslow, name='MACD_%d_%d' % (n_fast, n_slow))
    MACDsign = pd.Series(pd.ewma(MACD, span=9, min_periods=8), name='MACDsign_%d_%d' % (n_fast, n_slow))
    MACDdiff = pd.Series(MACD - MACDsign, name='MACDdiff_%d_%d' % (n_fast, n_slow))
    result = pd.DataFrame([MACD, MACDsign, MACDdiff]).transpose()
    return out(SETTINGS, df, result)


def MassI(df):
    """
    Mass Index
    """
    Range = df['high'] - df['low']
    EX1 = pd.ewma(Range, span=9, min_periods=8)
    EX2 = pd.ewma(EX1, span=9, min_periods=8)
    Mass = EX1 / EX2
    result = pd.Series(pd.rolling_sum(Mass, 25), name='Mass Index')
    return out(SETTINGS, df, result)


def Vortex(df, n):
    """
    Vortex Indicator
    """
    i = 0
    TR = [0]
    while i < len(df) - 1:  # df.index[-1]:
        Range = max(df.get_value(i + 1, 'high'), df.get_value(i, 'close')) - min(df.get_value(i + 1, 'low'), df.get_value(i, 'close'))
        TR.append(Range)
        i = i + 1
    i = 0
    VM = [0]
    while i < len(df) - 1:  # df.index[-1]:
        Range = abs(df.get_value(i + 1, 'high') - df.get_value(i, 'low')) - abs(df.get_value(i + 1, 'low') - df.get_value(i, 'high'))
        VM.append(Range)
        i = i + 1
    result = pd.Series(pd.rolling_sum(pd.Series(VM), n) / pd.rolling_sum(pd.Series(TR), n), name='Vortex_' + str(n))
    return out(SETTINGS, df, result)


def KST(df, r1, r2, r3, r4, n1, n2, n3, n4):
    """
    KST Oscillator
    """
    M = df['close'].diff(r1 - 1)
    N = df['close'].shift(r1 - 1)
    ROC1 = M / N
    M = df['close'].diff(r2 - 1)
    N = df['close'].shift(r2 - 1)
    ROC2 = M / N
    M = df['close'].diff(r3 - 1)
    N = df['close'].shift(r3 - 1)
    ROC3 = M / N
    M = df['close'].diff(r4 - 1)
    N = df['close'].shift(r4 - 1)
    ROC4 = M / N
    result = pd.Series(pd.rolling_sum(ROC1, n1) + pd.rolling_sum(ROC2, n2) * 2 + pd.rolling_sum(ROC3, n3) * 3 + pd.rolling_sum(ROC4, n4) * 4, name='KST_' + str(r1) + '_' + str(r2) + '_' + str(r3) + '_' + str(r4) + '_' + str(n1) + '_' + str(n2) + '_' + str(n3) + '_' + str(n4))
    return out(SETTINGS, df, result)


def RSI(df, n):
    """
    Relative Strength Index
    """
    i = 0
    UpI = [0]
    DoI = [0]
    while i + 1 <= len(df) - 1:  # df.index[-1]
        UpMove = df.get_value(i + 1, 'high') - df.get_value(i, 'high')
        DoMove = df.get_value(i, 'low') - df.get_value(i + 1, 'low')
        if UpMove > DoMove and UpMove > 0:
            UpD = UpMove
        else:
            UpD = 0
        UpI.append(UpD)
        if DoMove > UpMove and DoMove > 0:
            DoD = DoMove
        else:
            DoD = 0
        DoI.append(DoD)
        i = i + 1
    UpI = pd.Series(UpI)
    DoI = pd.Series(DoI)
    PosDI = pd.Series(pd.ewma(UpI, span=n, min_periods=n - 1))
    NegDI = pd.Series(pd.ewma(DoI, span=n, min_periods=n - 1))
    result = pd.Series(PosDI / (PosDI + NegDI), name='RSI_' + str(n))
    return out(SETTINGS, df, result)


def TSI(df, r, s):
    """
    True Strength Index
    """
    M = pd.Series(df['close'].diff(1))
    aM = abs(M)
    EMA1 = pd.Series(pd.ewma(M, span=r, min_periods=r - 1))
    aEMA1 = pd.Series(pd.ewma(aM, span=r, min_periods=r - 1))
    EMA2 = pd.Series(pd.ewma(EMA1, span=s, min_periods=s - 1))
    aEMA2 = pd.Series(pd.ewma(aEMA1, span=s, min_periods=s - 1))
    result = pd.Series(EMA2 / aEMA2, name='TSI_' + str(r) + '_' + str(s))
    return out(SETTINGS, df, result)


def ACCDIST(df, n):
    """
    Accumulation/Distribution
    """
    ad = (2 * df['close'] - df['high'] - df['low']) / (df['high'] - df['low']) * df['volume']
    M = ad.diff(n - 1)
    N = ad.shift(n - 1)
    ROC = M / N
    result = pd.Series(ROC, name='Acc/Dist_ROC_' + str(n))
    return out(SETTINGS, df, result)


def Chaikin(df):
    """
    Chaikin Oscillator
    """
    ad = (2 * df['close'] - df['high'] - df['low']) / (df['high'] - df['low']) * df['volume']
    result = pd.Series(pd.ewma(ad, span=3, min_periods=2) - pd.ewma(ad, span=10, min_periods=9), name='Chaikin')
    return out(SETTINGS, df, result)


def MFI(df, n):
    """
    Money Flow Index and Ratio
    """
    PP = (df['high'] + df['low'] + df['close']) / 3
    i = 0
    PosMF = [0]
    while i < len(df) - 1:  # df.index[-1]:
        if PP[i + 1] > PP[i]:
            PosMF.append(PP[i + 1] * df.get_value(i + 1, 'volume'))
        else:
            PosMF.append(0)
        i=i + 1
    PosMF = pd.Series(PosMF)
    TotMF = PP * df['volume']
    MFR = pd.Series(PosMF / TotMF)
    result = pd.Series(pd.rolling_mean(MFR, n), name='MFI_' + str(n))
    return out(SETTINGS, df, result)


def OBV(df, n):
    """
    On-balance Volume
    """
    i = 0
    OBV = [0]
    while i < len(df) - 1:  # df.index[-1]:
        if df.get_value(i + 1, 'close') - df.get_value(i, 'close') > 0:
            OBV.append(df.get_value(i + 1, 'volume'))
        if df.get_value(i + 1, 'close') - df.get_value(i, 'close') == 0:
            OBV.append(0)
        if df.get_value(i + 1, 'close') - df.get_value(i, 'close') < 0:
            OBV.append(-df.get_value(i + 1, 'volume'))
        i = i + 1
    OBV = pd.Series(OBV)
    result = pd.Series(pd.rolling_mean(OBV, n), name='OBV_' + str(n))
    return out(SETTINGS, df, result)


def FORCE(df, n):
    """
    Force Index
    """
    result = pd.Series(df['close'].diff(n) * df['volume'].diff(n), name='Force_' + str(n))
    return out(SETTINGS, df, result)


def EOM(df, n):
    """
    Ease of Movement
    """
    EoM = (df['high'].diff(1) + df['low'].diff(1)) * (df['high'] - df['low']) / (2 * df['volume'])
    result = pd.Series(pd.rolling_mean(EoM, n), name='EoM_' + str(n))
    return out(SETTINGS, df, result)


def CCI(df, n):
    """
    Commodity Channel Index
    """
    PP = (df['high'] + df['low'] + df['close']) / 3
    result = pd.Series((PP - pd.rolling_mean(PP, n)) / pd.rolling_std(PP, n), name='CCI_' + str(n))
    return out(SETTINGS, df, result)


def COPP(df, n):
    """
    Coppock Curve
    """
    M = df['close'].diff(int(n * 11 / 10) - 1)
    N = df['close'].shift(int(n * 11 / 10) - 1)
    ROC1 = M / N
    M = df['close'].diff(int(n * 14 / 10) - 1)
    N = df['close'].shift(int(n * 14 / 10) - 1)
    ROC2 = M / N
    result = pd.Series(pd.ewma(ROC1 + ROC2, span=n, min_periods=n), name='Copp_' + str(n))
    return out(SETTINGS, df, result)


def KELCH(df, n):
    """
    Keltner Channel
    """
    KelChM = pd.Series(pd.rolling_mean((df['high'] + df['low'] + df['close']) / 3, n), name='KelChM_' + str(n))
    KelChU = pd.Series(pd.rolling_mean((4 * df['high'] - 2 * df['low'] + df['close']) / 3, n), name='KelChU_' + str(n))
    KelChD = pd.Series(pd.rolling_mean((-2 * df['high'] + 4 * df['low'] + df['close']) / 3, n), name='KelChD_' + str(n))
    result = pd.DataFrame([KelChM, KelChU, KelChD]).transpose()
    return out(SETTINGS, df, result)


def ULTOSC(df):
    """
    Ultimate Oscillator
    """
    i = 0
    TR_l = [0]
    BP_l = [0]
    while i < len(df) - 1:  # df.index[-1]:
        TR = max(df.get_value(i + 1, 'high'), df.get_value(i, 'close')) - min(df.get_value(i + 1, 'low'), df.get_value(i, 'close'))
        TR_l.append(TR)
        BP = df.get_value(i + 1, 'close') - min(df.get_value(i + 1, 'low'), df.get_value(i, 'close'))
        BP_l.append(BP)
        i = i + 1
    result = pd.Series((4 * pd.rolling_sum(pd.Series(BP_l), 7) / pd.rolling_sum(pd.Series(TR_l), 7)) + (2 * pd.rolling_sum(pd.Series(BP_l), 14) / pd.rolling_sum(pd.Series(TR_l), 14)) + (pd.rolling_sum(pd.Series(BP_l), 28) / pd.rolling_sum(pd.Series(TR_l), 28)), name='Ultimate_Osc')
    return out(SETTINGS, df, result)


def DONCH(df, n):
    """
    Donchian Channel
    """
    i = 0
    DC_l = []
    while i < n - 1:
        DC_l.append(0)
        i = i + 1
    i = 0
    while i + n - 1 < len(df) - 1:  # df.index[-1]:
        DC = max(df['high'].ix[i:i + n - 1]) - min(df['low'].ix[i:i + n - 1])
        DC_l.append(DC)
        i = i + 1
    DonCh = pd.Series(DC_l, name='Donchian_' + str(n))
    result = DonCh.shift(n - 1)
    return out(SETTINGS, df, result)


def STDDEV(df, n):
    """
    Standard Deviation
    """
    result = pd.Series(pd.rolling_std(df['close'], n), name='STD_' + str(n))
    return out(SETTINGS, df, result)
