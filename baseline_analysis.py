import pandas as pd
import random

rooms_df = pd.read_csv('rooms.csv')
courses_df = pd.read_csv('courses.csv')

# Time representation: 7.5 = 7:30 AM, 9.0 = 9:00 AM
lecture_slots = [7.5, 9.0, 10.5, 12.0, 13.5, 15.0, 16.5, 18.0, 19.5]
lab_slots = [7.5, 12.0, 16.5]

baseline_schedule = []

for _, course in courses_df.iterrows():
    # Pick a random room
    room = rooms_df.sample(1).iloc[0]
    
    # Intentionally skew towards peak hours (e.g. 10:30, 12:00, 13:30, 15:00)
    if course['contact_hours'] == 4.5:
        if random.random() < 0.6:
            start_time = 12.0
        else:
            start_time = random.choice([7.5, 16.5])
    else: # 1.5 hours
        if random.random() < 0.7:
            start_time = random.choice([10.5, 12.0, 13.5, 15.0])
        else:
            start_time = random.choice([7.5, 9.0, 16.5, 18.0, 19.5])
            
    baseline_schedule.append({
        'course_id': course['course_id'],
        'section': course['section'],
        'department': course['department'],
        'enrollment': course['enrollment'],
        'contact_hours': course['contact_hours'],
        'assigned_room': room['room_id'],
        'room_type': room['room_type'],
        'room_capacity': room['capacity'],
        'start_time': start_time
    })

baseline_df = pd.DataFrame(baseline_schedule)
baseline_df.to_csv('baseline_schedule.csv', index=False)

print("--- NEW BASELINE SCHEDULE ANALYSIS ---")

peak_classes = baseline_df[(baseline_df['start_time'] >= 10.5) & (baseline_df['start_time'] <= 15.0)]
peak_percentage = (len(peak_classes) / len(baseline_df)) * 100
print(f"1. Peak Hour Concentration (10:30am-4:30pm): {peak_percentage:.1f}% of classes")

baseline_df['seat_utilization'] = (baseline_df['enrollment'] / baseline_df['room_capacity']) * 100
avg_seat_util = baseline_df['seat_utilization'].mean()
print(f"2. Average Seat Utilization: {avg_seat_util:.1f}%")

# Facility Mismatch Check
mismatches = baseline_df[
    (baseline_df['contact_hours'] == 4.5) & (baseline_df['room_type'] == 'Lecture Room')
]
print(f"3. Facility Mismatches: {len(mismatches)} lab classes scheduled in normal Lecture Rooms")

print("\n--- DEPARTMENT CLASSROOM DEMAND (Hours) ---")
dept_demand = courses_df.groupby('department')['contact_hours'].sum().reset_index()
dept_demand.columns = ['Department', 'Total Hours Needed']
print(dept_demand.to_string(index=False))
