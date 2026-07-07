#!/usr/bin/env python3
import os
import sys
import logging
import subprocess

logging.basicConfig(
	level=logging.INFO,
	format='%(asctime)s [%(levelname)s] %(message)s',
	handlers=[
		logging.FileHandler("/var/log/burnin.log"),
		logging.StreamHandler(sys.stdout)
		]
	)

MIN_CPUS  = 2
MIN_RAM_GB = 4

def run_burnin():
	logging.info("=== STARTING HARDWARE VALIDATION ===")
	
	cpu_count = os.cpu_count()
	
	ram_gb = 0
	if os.path.exists('/proc/meminfo'):
		with open('/proc/meminfo', 'r') as f:
			for line in f:
				if 'MemTotal' in line:
					ram_kb = int(line.split()[1])
					ram_gb = round(ram_kb / (1024*1024))
					break

	logging.info(f"Detected specs: {cpu_count} CPU(s), {ram_gb} GB RAM.")
	if cpu_count < MIN_CPUS or ram_gb < MIN_RAM_GB:
		logging.error(f"CRITICAL MISMATCH: System specs do not meet requirements")
		sys.exit(1)

	logging.info("HARDWARE VERIFIED. Launching workload profiling (stress-ng)...")

	stress_command = [ "stress-ng", "--cpu", str(cpu_count), "--io", "2", "--vm", "1", "--vm-bytes", "512M", "--timeout", "1m"]

	try:
		process =  subprocess.run(stress_command, capture_output=True, text=True, check=True)
		logging.info("=== BURN-IN COMPLETE===")
		logging.info(process.stdout)

	except subprocess.CalledProcessError as e:
		logging.error(f"stress-ng execution exception: {e.stderr}")
		sys.exit(1)

if __name__ == "__main__":
	run_burnin()
