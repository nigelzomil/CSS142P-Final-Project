import pandas as pd
import random

random.seed(42)

# Generate Rooms
rooms_data = []
# Create 15 MPO rooms
for _ in range(15):
    floor = random.randint(1, 6)
    room_num = random.randint(1, 25)
    room_id = f"MPO{floor}{room_num:02d}"
    
    # 30% chance to be a lab, 70% lecture
    if random.random() < 0.3:
        room_type = random.choice(["Computer Lab", "Multimedia Lab", "Nursing Lab", "Science Lab"])
        capacity = random.choice([25, 30, 40])
    else:
        room_type = "Lecture Room"
        capacity = random.choice([40, 50, 80, 100])
        
    rooms_data.append({"room_id": room_id, "capacity": capacity, "room_type": room_type})

# Add Cervantes room
rooms_data.append({"room_id": "Cervantes Room", "capacity": 60, "room_type": "Lecture Room"})

pd.DataFrame(rooms_data).to_csv("rooms.csv", index=False)

# Generate Courses
departments = [
    "School of Information Technology",
    "E.T. Yuchengco School of Business Management",
    "School of Multimedia and Digital Arts",
    "School of Nursing",
    "School of Health Sciences"
]

courses = []
course_id_counter = 100

for dept in departments:
    num_courses = random.randint(4, 7)
    for c in range(1, num_courses + 1):
        # Create course id prefix based on dept (e.g., SIT, ETYSBM)
        prefix = "".join([word[0] for word in dept.split() if word.lower() not in ['of', 'and']]).upper()
        if "YUCHENGCO" in dept.upper(): prefix = "ETYSBM"
        
        course_num = f"{prefix}-{course_id_counter}"
        course_id_counter += 1
        
        num_sections = random.randint(1, 3)
        for s in range(num_sections):
            section = chr(65 + s)
            
            # Determine if lab or lecture
            is_lab = False
            req_type = "Lecture Room"
            if dept == "School of Information Technology" and random.random() < 0.5:
                is_lab = True
                req_type = "Computer Lab"
            elif dept == "School of Multimedia and Digital Arts" and random.random() < 0.5:
                is_lab = True
                req_type = "Multimedia Lab"
            elif dept == "School of Nursing" and random.random() < 0.4:
                is_lab = True
                req_type = "Nursing Lab"
            elif dept == "School of Health Sciences" and random.random() < 0.4:
                is_lab = True
                req_type = "Science Lab"
                
            hours = 4.5 if is_lab else 1.5
            enrollment = random.randint(20, 45) if is_lab else random.randint(30, 80)
            
            courses.append({
                "course_id": course_num,
                "department": dept,
                "section": section,
                "enrollment": enrollment,
                "contact_hours": hours,
                "required_room_type": req_type
            })

pd.DataFrame(courses).to_csv("courses.csv", index=False)
print(f"Generated {len(rooms_data)} rooms and {len(courses)} course sections with updated university specifications.")
