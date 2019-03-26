import os
from datetime import datetime

cwd = os.getcwd()
files = [file for file in os.listdir(cwd)
         if file.endswith("Test.py") and not file.startswith("BacktestRequest")]
start = datetime.now()

i = 1
for file in files:
    print(f"Running test No. {i}: {file}")
    os.system(f"python -m unittest discover -p \"*{file}\"")
    if file == 'AuthorSearchTest.py':
        i += 11
    elif file == "AlphaSearchTest.py":
        i+= 9
    else:
        i += 1

print(f'Total time elapsed for {i} tests: {(datetime.now() - start).total_seconds()} s')