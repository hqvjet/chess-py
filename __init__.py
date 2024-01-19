import subprocess

try:
    subprocess.run(['python3', 'server/__init__.py'], check=True)
    subprocess.run(['python3', 'client/__init__.py'], check=True)
except subprocess.CalledProcessError as e:
    print(f"Error: {e}")
