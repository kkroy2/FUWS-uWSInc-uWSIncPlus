import sns as sns
from scipy.stats import norm
# generate random numbers from N(0,1)
data_normal = norm.rvs(size=100, loc=0.5, scale=0.1)
std_dv = [0.05, 0.1, 0.125, 0.15, 0.25]
file = ['prob_5_05.csv', 'prob_5_1.csv', 'prob_5_125.csv', 'prob_5_15.csv', 'prob_5_25.csv']
# file = ['wgt_5_05.csv', 'wgt_5_1.csv', 'wgt_5_125.csv', 'wgt_5_15.csv', 'wgt_5_25.csv']
i = 0
for dv in std_dv:
    prob_data = norm.rvs(size=1000000,  loc=0.5, scale=dv)

    cur_file = open(file[i], 'w')
    i += 1
    for ch_dt in prob_data:
        if (ch_dt <= 0.0001) or (ch_dt >= .9999):
            continue
        cur_file.write(str(round(ch_dt, 3)))
        cur_file.write('\n')
    cur_file.close()



# print(data_normal)
# ax = sns.displot(data_normal,
#                   bins=100,
#                   kde=True,
#                   color='skyblue',
#                   hist_kws={"linewidth": 15,'alpha':1})
# ax.set(xlabel='Normal Distribution', ylabel='Frequency')
