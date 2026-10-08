import subprocess
import sys

scripts = [
    ("Stage 1: Mock Data Generation", "generate_mock_data.py"),
    ("Stage 2: Baseline Schedule Analysis", "baseline_analysis.py"),
    ("Stage 3: Static Schedule Optimization", "static_scheduler.py"),
    ("Stage 4: SimPy Discrete-Event Simulation", "simpy_stress_test.py"),
    ("Stage 5: Generating KPI Visualizations", "generate_visualizations.py"),
    ("Stage 6: Generating Usage Visualizations", "generate_additional_visualizations.py")
]

print("\n" + "="*60)
print(" STARTING UNIVERSITY SCHEDULING PIPELINE")
print("="*60)

for step_name, script_file in scripts:
    print(f"\n>>> Running {step_name} ({script_file})...")
    try:
        # Run the script and print its output directly to the console
        subprocess.run([sys.executable, script_file], check=True)
    except subprocess.CalledProcessError:
        print(f"\n[ERROR] Pipeline halted. '{script_file}' encountered an error.")
        sys.exit(1)

print("\n" + "="*60)
print(" PIPELINE COMPLETE!")
print(" All datasets (.csv) and charts (.png) have been updated.")
print("="*60 + "\n")
