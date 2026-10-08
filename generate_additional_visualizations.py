import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# 1. Department Allocation Visualization
optimized_df = pd.read_csv('optimized_schedule.csv')
dept_usage = optimized_df.groupby('department')['contact_hours'].sum().sort_values()

plt.figure(figsize=(10, 6))
dept_usage.plot(kind='barh', color='#8fbcd4', edgecolor='black')
plt.title('Total Classroom Hours Allocated per Department')
plt.xlabel('Total Allocated Hours')
plt.ylabel('')
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('department_usage.png')
plt.close()

# 2. Stress Test Results Visualization
# Using the exact metrics from our SimPy simulation
scenarios = ['Low Demand', 'Medium Demand', 'High Demand']
requests = [5, 12, 20]
accommodated = [5, 12, 20]

x = np.arange(len(scenarios))
width = 0.35

fig, ax = plt.subplots(figsize=(8, 5))
rects1 = ax.bar(x - width/2, requests, width, label='Ad-Hoc Requests Generated', color='#ffb366', edgecolor='black')
rects2 = ax.bar(x + width/2, accommodated, width, label='Requests Accommodated (100% Success)', color='#99ff99', edgecolor='black')

ax.set_ylabel('Number of Room Requests')
ax.set_title('SimPy Stress Test: Schedule Resilience')
ax.set_xticks(x)
ax.set_xticklabels(scenarios)
ax.legend(loc='upper left')

def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)

plt.tight_layout()
plt.savefig('stress_test_results.png')
plt.close()

print("Generated department_usage.png and stress_test_results.png")
