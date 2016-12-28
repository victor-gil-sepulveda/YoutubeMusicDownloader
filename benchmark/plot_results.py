import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

results = pd.read_csv('results_big.csv', header=0)
sns.set_style("whitegrid")
grouped = results.groupby("NumProcs")
means = grouped.mean()
std = grouped.std()

fig, ax = plt.subplots()
means.plot(yerr=std, ax=ax)
ax.set_ylabel("Time (s)")

plt.show()
