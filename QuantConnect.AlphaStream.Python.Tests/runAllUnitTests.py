import os
from datetime import datetime
from time import sleep

cwd = os.getcwd()
files = [file for file in os.listdir(cwd)
         if file.endswith("Test.py") and not file.startswith("BacktestRequest")]

i = 1
start = datetime.now()
for file in files:
    print(f'Running {file}')
    os.system(f"python -m unittest discover -p \"*{file}\"")
print(f'Total time elapsed: {(datetime.now() - start).total_seconds()} s')