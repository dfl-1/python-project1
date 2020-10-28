'''acorr_ljungbox(x, lags=None, boxpierce=False)函数检验无自相关
lags为延迟期数，若为None则输出min((nobs // 2 - 2), 40)，其中nobs为观测样本数量，样本较大的情况下输出40
boxpierce为True时表示除开返回LB统计量还会返回Box和Pierce的Q统计量
返回值：
lbvalue:测试的统计量
pvalue:基于卡方分布的p统计量
bpvalue:((optionsal), float or array) – test statistic for Box-Pierce test
bppvalue:((optional), float or array) – p-value based for Box-Pierce test on chi-square distribution'''
from pandas import np
from statsmodels.stats.diagnostic import acorr_ljungbox


def test_stochastic(ts,lag):
    p_value = acorr_ljungbox(ts, lags=lag) #lags可自定义
    return p_value


data = np.random.normal(size=1000)
d=[1,2,3,4,5,60,100,80,9,10,11,12]
d2=[1,2,3,4]
print(acorr_ljungbox(d2,[x for x in range(1,len(d2))]))
