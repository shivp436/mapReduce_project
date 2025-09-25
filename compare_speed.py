import subprocess

scripts = ["serial_processing.py", "parallel_processing.py"]

for script in scripts:
    print(f"\n--- Running {script} ---\n")
    # Run the script, inherit stdout/stderr so their prints show here
    subprocess.run(["python", script], check=True)

