# Preliminaries
import math
import numpy as np
import pandas as pd
import warnings
from scipy.stats import t
from scipy.stats import pearsonr


# main function

# uncertain t test
def uncertain_t(v,tail,value):
    '''
    input vector should be a np.array, v=(x,p), x stands for value, p stands for prob to be in group 1 //
    tail should be 1 or 2, means 1 tailed t-test or 2 tailed t-test //
    value should be 'test_statistics' or 'p_value'
    '''
    x, p = np.hsplit(v, 2)
    N = len(x)
    p_hat = np.mean(p)
    V_p = np.var(p,ddof=0)
    d = sum((p-p_hat)*x)/(N*V_p) # unbiased estimator of mu1-mu2
    sig2_hat = (sum((x-np.mean(x))**2) - N*p_hat*(1-p_hat)*d**2)/(N-2) # estimator of sigma
    output = pd.DataFrame(columns=['test_statistics', 'p_value'])
    if sig2_hat <= 0: # some sigma2 could be negative
        output.loc[0, 'test_statistics'] = pearsonr(x.reshape(N), p.reshape(N), alternative = 'greater')[0]
        output.loc[1, 'test_statistics'] = pearsonr(x.reshape(N), p.reshape(N))[0]
        output.loc[0, 'p_value'] = min(pearsonr(x.reshape(N), p.reshape(N), alternative = 'greater')[1], pearsonr(x.reshape(N), p.reshape(N), alternative = 'less')[1])
        output.loc[1, 'p_value'] = pearsonr(x.reshape(N), p.reshape(N))[1]
        warnings.warn("Variance of test-statistics is less or equal to 0", Warning)
    else:
        output['test_statistics'] = (d*math.sqrt(N*V_p/sig2_hat), abs(d*math.sqrt(N*V_p/sig2_hat)))
        output.loc[0,'p_value'] = min(1-t.cdf(x=output.loc[0,'test_statistics'],df=N-1), t.cdf(x=output.loc[0,'test_statistics'],df=N-1))
        output.loc[1,'p_value'] = 2*(1-t.cdf(x=output.loc[1,'test_statistics'],df=N-1)) # degree fredom N-1
    return output.loc[tail-1,value]



# estimate the mean and the standard error of two groups
def estimates(v, value='all'):
    '''
    value controls the return, 'mean' for mean, 'standard_error' for se, default is all
    input vector should be a np.array, v=(x,p), x stands for value, p stands for prob to be in group 1 //
    '''
    x,p=np.hsplit(v,2)
    N=len(x)
    p_hat=np.mean(p)
    V_p=np.var(p,ddof=0)
    d=sum((p-p_hat)*x)/(N*V_p)
    mu1 = np.mean(x) + d*(1-p_hat)
    mu2 = np.mean(x) - d*p_hat
    z = np.sum((p-p_hat)*x**2)
    se1 = np.sqrt((sum(x**2)/N- (1-p_hat)*z/(N*V_p)) - mu1**2)
    se2 = np.sqrt((sum(x**2)/N- p_hat*z/(N*V_p)) - mu2**2)
    if value == 'all':
        return np.array([mu1, se1, mu2, se2]).reshape(4)
    elif value == 'standard_error':
        return np.array([se1, se2]).reshape(2)
    else:
        return np.array([mu1, mu2]).reshape(2)



# preprocess the data set
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

    # transform the feature value
    v[df.loc[df.iloc[:,1]==1].index,0]=prob[1]
    v[df.loc[df.iloc[:,1]==0].index,0]=1-prob[1]
    return v


# single test for all features
def multiple_test(featurelist,groupvariable,dataset,accuracy_vec):
    '''
    featurelist, features to be test //
    accuracy_vec is the accuracy of one groupvariable and all the features //
    accuracy_vec = (g,f1,f2,...,fn), g represents accuracy the groupvariable //
    it returns unadjuested p-values of all single tests
    '''
    p_value=np.ones(shape=(len(featurelist)))
    for i in range(len(featurelist)):
        df_temp=dataset[[groupvariable,featurelist[i]]]
        v=dfprocess(df_temp,[accuracy_vec[0],accuracy_vec[i+1]])
        p_value[i]=uncertain_t(v,2,'p_value')
    return p_value


# estimates of mean, se for all features
def multiple_estimates(featurelist,groupvariable,dataset,accuracy_vec):
    '''
    featurelist, features to be test //
    accuracy_vec is the accuracy of one groupvariable and all the features //
    accuracy_vec = (g,f1,f2,...,fn), g represents accuracy of the group variable //
    it returns estimate mean, se of all features
    '''
    output=pd.DataFrame(columns=['feature','mean1','se1','mean2','se2'])
    output['feature']=featurelist
    for i in range(len(featurelist)):
        df_temp=dataset[[groupvariable,featurelist[i]]]
        v=dfprocess(df_temp,[accuracy_vec[0],accuracy_vec[i+1]])
        output.loc[i,['mean1','se1','mean2','se2']] = estimates(v, value='all')
    return output


# adjust the p-value
def holm(pvals, p_value=True, alpha=0.05):
    '''
    pvals is the list of p-values //
    p_value, control it returns the adjusted p-value or rejected results //
    alpha is FWER, family-wise error rate, e.g. 0.05
    '''
    index=np.argsort(pvals)
    pval_ordered=pvals[index]
    m=len(pvals)
    for i in range(m):
        if i==0:
            pval_ordered[i] = m*pval_ordered[i]
        else:
            pval_ordered[i] = max(pval_ordered[i-1],(m-i)*pval_ordered[i])
    new_pvals=pval_ordered[np.argsort(index)]
    if p_value:
        return new_pvals
    else:
        output=[]
        for i in range(m):
            if new_pvals[i] <= alpha:
                output.append('Reject null hypothesis')
            else:
                output.append('Accept null hypothesis')
        return output

# calculate effect size based on estimated proportions
def effect_size(p):
    '''
    p = (p1, p2), represents estimated proportions in two groups //
    it returns cohen'h of p1-p2
    '''
    if any(p < 0):
        return ('Proportion should not less than 0')
    else:
        varphi1 = 2*math.asin(math.sqrt(p[0]))
        varphi2 = 2*math.asin(math.sqrt(p[1]))
        return varphi1 - varphi2