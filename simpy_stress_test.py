import pandas as pd
import simpy
import random

# Load the optimized schedule and rooms
try:
    schedule_df = pd.read_csv('optimized_schedule.csv')
    rooms_df = pd.read_csv('rooms.csv')
except FileNotFoundError:
    print("Error: Could not find optimized_schedule.csv. Please run static_scheduler.py first.")
    exit()

# Helper function to convert 24hr float time to simulation ticks (0 = 7:30 AM, 13.5 = 9:00 PM)
def to_env_time(real_time):
    return real_time - 7.5

class UniversitySim:
    def __init__(self, env, stress_level="medium"):
        self.env = env
        self.rooms = {}
        # Create a PriorityResource for each room
        for _, room in rooms_df.iterrows():
            self.rooms[room['room_id']] = {
                'resource': simpy.PriorityResource(env, capacity=1),
                'type': room['room_type']
            }
        
        self.ad_hoc_requests = 0
        self.ad_hoc_granted = 0
        
        # Arrival rate of unexpected requests (e.g., makeup classes, club meetings)
        if stress_level == "low":
            self.arrival_interval = 3.0   # Avg 1 request every 3 hours
        elif stress_level == "medium":
            self.arrival_interval = 1.5   # Avg 1 request every 1.5 hours
        else: # high
            self.arrival_interval = 0.5   # Avg 1 request every 30 mins
            
    def regular_class(self, course_id, room_id, start_time, duration):
        """Simulate a regularly scheduled class occupying a room"""
        env_start = to_env_time(start_time)
        
        # Wait until it's time for the class to start
        if env_start > self.env.now:
            yield self.env.timeout(env_start - self.env.now)
        
        # Request the room (Priority 1 - highest, because it's on the master schedule)
        with self.rooms[room_id]['resource'].request(priority=1) as req:
            yield req
            # Occupy the room for the duration of the class
            yield self.env.timeout(duration)

    def ad_hoc_generator(self):
        """Generate random, unexpected room requests during the day"""
        while True:
            # Wait a random amount of time before the next request arrives
            yield self.env.timeout(random.expovariate(1.0 / self.arrival_interval))
            
            # Don't generate new requests after 7:30 PM (12 hours into the day)
            if self.env.now > 12.0: 
                break
                
            self.ad_hoc_requests += 1
            req_type = "Lecture Room" # Assume most unexpected requests just need a standard room
            req_duration = 1.5
            
            # Attempt to find an available room at THIS EXACT MOMENT
            granted = False
            for r_id, room_data in self.rooms.items():
                # If the room is the right type and currently empty
                if room_data['type'] == req_type and room_data['resource'].count == 0:
                    self.env.process(self.handle_ad_hoc(r_id, req_duration))
                    self.ad_hoc_granted += 1
                    granted = True
                    break # Room found, stop looking

    def handle_ad_hoc(self, room_id, duration):
        """Process an approved ad-hoc request"""
        # Priority 2 - lower than regular classes
        with self.rooms[room_id]['resource'].request(priority=2) as req:
            yield req
            yield self.env.timeout(duration)

def run_stress_test(stress_level):
    env = simpy.Environment()
    uni = UniversitySim(env, stress_level=stress_level)
    
    # 1. Pre-load the Master Schedule into the simulation
    for _, row in schedule_df.iterrows():
        env.process(uni.regular_class(
            row['course_id'], 
            row['assigned_room'], 
            row['start_time'], 
            row['contact_hours']
        ))
        
    # 2. Start the unexpected event generator
    env.process(uni.ad_hoc_generator())
    
    # 3. Run the simulation for the operating day (13.5 hours)
    env.run(until=13.5)
    
    success_rate = (uni.ad_hoc_granted / uni.ad_hoc_requests * 100) if uni.ad_hoc_requests > 0 else 0
    print(f"--- STRESS TEST: {stress_level.upper()} DEMAND ---")
    print(f"Total Unexpected Requests: {uni.ad_hoc_requests}")
    print(f"Requests Accommodated: {uni.ad_hoc_granted}")
    print(f"Schedule Resilience Rate: {success_rate:.1f}%\n")

random.seed(42)
print("Simulating a 13.5-hour operating day based on the optimized Master Schedule...\n")
run_stress_test("low")
run_stress_test("medium")
run_stress_test("high")
