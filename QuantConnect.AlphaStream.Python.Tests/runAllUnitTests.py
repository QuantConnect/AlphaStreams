import os
from datetime import datetime
from time import sleep

cwd = os.getcwd()
files = [file for file in os.listdir(cwd)
         if file.endswith("Test.py") and not file.startswith("BacktestRequest")]

i = 1
start = datetime.now()
for file in files:
    if file == 'AuthorSearchTest.py' or file =="AlphaSearchTest.py":
        print(f"Running test No. {i} through {i+9} -- {file}")
        os.system(f"python -m unittest discover -p \"*{file}\"")
        i += 10
    else:
        print(f"Running test No. {i} -- {file}")
        os.system(f"python -m unittest discover -p \"*{file}\"")
        i += 1
print(f'Total time elapsed for {i} tests: {(datetime.now() - start).total_seconds()} s')