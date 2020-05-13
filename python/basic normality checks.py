# -*- coding: utf-8 -*-
"""
Trumann
Tue May 12 20:48:49 2020
"""

from scipy.stats import shapiro, normaltest, anderson

# =============================================================================
# # normality test
# stat, p = shapiro(a_arr)
# print('Statistics=%.3f, p=%.3f' % (stat, p))
# # interpret
# alpha = 0.05
# if p > alpha:
# 	print('Sample looks Gaussian (fail to reject H0)')
# else:
# 	print('Sample does not look Gaussian (reject H0)') <-- result
# =============================================================================
    
# =============================================================================
# # normality test
# stat, p = normaltest(a_arr)
# print('Statistics=%.3f, p=%.3f' % (stat, p))
# # interpret
# alpha = 0.05
# if p > alpha:
# 	print('Sample looks Gaussian (fail to reject H0)')
# else:
# 	print('Sample does not look Gaussian (reject H0)') <-- result
# =============================================================================

# =============================================================================
# # normality test
# result = anderson(a_arr)
# print('Statistic: %.3f' % result.statistic)
# p = 0
# for i in range(len(result.critical_values)):
# 	sl, cv = result.significance_level[i], result.critical_values[i]
# 	if result.statistic < result.critical_values[i]:
# 		print('%.3f: %.3f, data looks normal (fail to reject H0)' % (sl, cv))
# 	else:
# 		print('%.3f: %.3f, data does not look normal (reject H0)' % (sl, cv))
# result: failed normality at every significance level...
# =============================================================================