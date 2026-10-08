import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load schedules
baseline_df = pd.read_csv('baseline_schedule.csv')
optimized_df = pd.read_csv('optimized_schedule.csv')

# --- Metric calculations ---
# 1. Peak Hour Concentration
base_peak = len(baseline_df[(baseline_df['start_time'] >= 10.5) & (baseline_df['start_time'] <= 15.0)])
base_peak_pct = (base_peak / len(baseline_df)) * 100

opt_peak = len(optimized_df[(optimized_df['start_time'] >= 10.5) & (optimized_df['start_time'] <= 15.0)])
opt_peak_pct = (opt_peak / len(optimized_df)) * 100

# 2. Average Seat Utilization
baseline_df['seat_utilization'] = (baseline_df['enrollment'] / baseline_df['room_capacity']) * 100
base_util = baseline_df['seat_utilization'].mean()

optimized_df['seat_utilization'] = (optimized_df['enrollment'] / optimized_df['room_capacity']) * 100
opt_util = optimized_df['seat_utilization'].mean()

# 3. Facility Mismatches
base_mismatch = len(baseline_df[(baseline_df['contact_hours'] == 4.5) & (baseline_df['room_type'] == 'Lecture Room')])
opt_mismatch = len(optimized_df[(optimized_df['contact_hours'] == 4.5) & (optimized_df['room_type'] == 'Lecture Room')])

# --- Chart 1: Key Performance Indicators ---
labels = ['Peak Hour %\n(Lower is better)', 'Seat Utilization %\n(Closer to 100 is better)', 'Facility Mismatches\n(Lower is better)']
baseline_metrics = [base_peak_pct, base_util, base_mismatch]
optimized_metrics = [opt_peak_pct, opt_util, opt_mismatch]

x = np.arange(len(labels))
width = 0.35

fig, ax = plt.subplots(figsize=(10, 6))
rects1 = ax.bar(x - width/2, baseline_metrics, width, label='Baseline Schedule', color='#ff9999')
rects2 = ax.bar(x + width/2, optimized_metrics, width, label='Optimized Schedule', color='#66b3ff')

ax.set_ylabel('Scores / Count')
ax.set_title('Classroom Optimization Results: Baseline vs. Optimized Model')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

# Add labels on top of bars
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height:.1f}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)

plt.tight_layout()
plt.savefig('optimization_metrics.png')
plt.close()

# --- Chart 2: Time Distribution of Classes ---
base_times = baseline_df['start_time']
opt_times = optimized_df['start_time']

bins = np.arange(7.5, 22.5, 1.5) # 1.5 hour bins up to 21.0

plt.figure(figsize=(10, 5))
plt.hist([base_times, opt_times], bins=bins, label=['Baseline', 'Optimized'], color=['#ff9999', '#66b3ff'], edgecolor='black')
plt.title('Class Start Time Distribution (Load Smoothing)')
plt.xlabel('Time of Day (7.5 = 7:30 AM, 19.5 = 7:30 PM)')
plt.ylabel('Number of Classes Starting')
plt.xticks(bins)
plt.legend()
plt.grid(axis='y', alpha=0.75)
plt.tight_layout()
plt.savefig('time_distribution.png')
plt.close()

print("Successfully generated 'optimization_metrics.png' and 'time_distribution.png'.")
