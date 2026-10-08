import pandas as pd

# Load data
rooms_df = pd.read_csv('rooms.csv')
courses_df = pd.read_csv('courses.csv')

# Time slots (7.5 = 7:30 AM, 21.0 = 9:00 PM)
lecture_slots = [7.5, 9.0, 10.5, 12.0, 13.5, 15.0, 16.5, 18.0, 19.5]
lab_slots = [7.5, 12.0, 16.5]

# Sort courses to schedule the hardest ones first:
# Labs first, then largest enrollment to smallest
courses_df = courses_df.sort_values(by=['contact_hours', 'enrollment'], ascending=[False, False])

# Dictionary to keep track of booked times for each room
room_schedules = {room['room_id']: [] for _, room in rooms_df.iterrows()}

scheduled_classes = []
unscheduled_classes = []

def is_room_free(room_id, start_time, end_time):
    """Check if the room is available between start_time and end_time"""
    for booked_start, booked_end in room_schedules[room_id]:
        # Overlap logic
        if start_time < booked_end and end_time > booked_start:
            return False
    return True

# Greedy Scheduling Algorithm
for _, course in courses_df.iterrows():
    scheduled = False
    
    # 1. Filter valid rooms: capacity must be enough, and facility type must match
    valid_rooms = rooms_df[
        (rooms_df['capacity'] >= course['enrollment']) & 
        (rooms_df['room_type'] == course['required_room_type'])
    ].sort_values(by='capacity') # Sort ascending by capacity to assign the SMALLEST valid room (better capacity matching)
    
    slots = lab_slots if course['contact_hours'] == 4.5 else lecture_slots
    
    for _, room in valid_rooms.iterrows():
        if scheduled: break
        
        for start in slots:
            end = start + course['contact_hours']
            if end > 21.0: # Do not schedule past 9:00 PM
                continue
                
            if is_room_free(room['room_id'], start, end):
                # Book the room
                room_schedules[room['room_id']].append((start, end))
                
                scheduled_classes.append({
                    'course_id': course['course_id'],
                    'section': course['section'],
                    'department': course['department'],
                    'enrollment': course['enrollment'],
                    'contact_hours': course['contact_hours'],
                    'assigned_room': room['room_id'],
                    'room_type': room['room_type'],
                    'room_capacity': room['capacity'],
                    'start_time': start
                })
                scheduled = True
                break
                
    if not scheduled:
        unscheduled_classes.append(course.to_dict())

optimized_df = pd.DataFrame(scheduled_classes)
optimized_df.to_csv('optimized_schedule.csv', index=False)

print("--- OPTIMIZED SCHEDULE ANALYSIS ---")
print(f"Total courses successfully scheduled: {len(scheduled_classes)} / {len(courses_df)}")
print(f"Total courses unscheduled: {len(unscheduled_classes)}\n")

if len(scheduled_classes) > 0:
    peak_classes = optimized_df[(optimized_df['start_time'] >= 10.5) & (optimized_df['start_time'] <= 15.0)]
    peak_percentage = (len(peak_classes) / len(optimized_df)) * 100
    print(f"1. Peak Hour Concentration (10:30am-4:30pm): {peak_percentage:.1f}% of classes")

    optimized_df['seat_utilization'] = (optimized_df['enrollment'] / optimized_df['room_capacity']) * 100
    avg_seat_util = optimized_df['seat_utilization'].mean()
    print(f"2. Average Seat Utilization: {avg_seat_util:.1f}%")

    mismatches = optimized_df[
        (optimized_df['contact_hours'] == 4.5) & (optimized_df['room_type'] == 'Lecture Room')
    ]
    print(f"3. Facility Mismatches: {len(mismatches)}")

if len(unscheduled_classes) > 0:
    print("\nWARNING: Some classes could not be scheduled due to lack of capacity/rooms:")
    for u in unscheduled_classes:
        print(f" - {u['course_id']} (Enrollment: {u['enrollment']}, Required: {u['required_room_type']})")
