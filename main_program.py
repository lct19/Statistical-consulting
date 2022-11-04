# Preliminaries
import math
import numpy as np
import pandas as pd
import warnings
from scipy.stats import t


# main function

# uncertain t test
def uncertain_t(v,tail,value):
    '''
    input vector should be a np.array, v=(x,p), x stands for value, p stands for prob to be in group 1 //
    tail should be 1 or 2, means 1 tailed t-test or 2 tailed t-test //
    value should be 'test_statistics' or 'p_value'
    '''
    x,p=np.hsplit(v,2)
    N=len(x)
    p_hat=np.mean(p)
    V_p=np.var(p,ddof=0)
    d=sum((p-p_hat)*x)/(N*V_p) # unbiased estimator of mu1-mu2
    sig2_hat=abs(sum((x-np.mean(x))**2)-N*p_hat*(1-p_hat)*d**2)/(N-2) # estimator of sigma
    output=pd.DataFrame(columns=['test_statistics','p_value'])
    if sig2_hat==0:
        output['test_statistics']=(float('inf'),float('inf'))
        output['p_value']=(1,1)
        warnings.warn("Variance of test-statistics is 0", Warning)
    else:
        output['test_statistics']=(d*math.sqrt(N*V_p/sig2_hat),abs(d*math.sqrt(N*V_p/sig2_hat)))
        output.loc[0,'p_value']=min(1-t.cdf(x=output.loc[0,'test_statistics'],df=N-1),t.cdf(x=output.loc[0,'test_statistics'],df=N-1))
        output.loc[1,'p_value']=2*(1-t.cdf(x=output.loc[1,'test_statistics'], df=N-1))
    return (output.loc[tail-1,value])


def dfprocess(df,prob):
    '''
    df is a (n,2) dataframe, first col is the group variable, second col is the feature to be compared //
    prob is the accuracy vector (p1, p2), p1 is the accuracy of group variable //
    it returns v=(x,p), p is the prob to be in group 1
    '''
    v=np.zeros(shape=(df.shape))
    # transform the group variable
    v[df.loc[df.iloc[:,0]==1].index,1]=prob[0]
    v[df.loc[df.iloc[:,0]==0].index,1]=1-prob[0]

    # transform the feature
    v[df.loc[df.iloc[:,1]==1].index,0]=prob[1]
    v[df.loc[df.iloc[:,1]==0].index,0]=1-prob[1]
    return v


def multiple_test(featurelist,groupvariable,dataset,prob):
    '''
    featurelist, features to be test //
    it returns unadjuested p-values of all single tests
    '''
    p_value=np.ones(shape=(len(featurelist)))
    for i in range(len(featurelist)):
        df_temp=dataset[[groupvariable,featurelist[i]]]
        v=dfprocess(df_temp,prob)
        p_value[i]=uncertain_t(v,2,'p_value')
    return p_value


def holm(pvals, alpha):
    '''
    pvals is the list of p-values //
    alpha is FWER, family-wise error rate, e.g. 0.1
    '''
    index=np.argsort(pvals)
    pval_ordered=pvals[index]
    m=len(pvals)
    threshold=1-(1-alpha)**(1/m)
    for i in range(m):
        if i==0:
            pval_ordered[i] = (m-i)*pval_ordered[i]
        else:
            pval_ordered[i] = max(pval_ordered[i-1],(m-i)*pval_ordered[i])
    new_pvals=pval_ordered[np.argsort(index)]
    output=[]
    for i in range(m):
        if new_pvals[i] <= threshold:
            output.append('Reject null hypothesis')
        else:
            output.append('Accept null hypothesis')
    return output