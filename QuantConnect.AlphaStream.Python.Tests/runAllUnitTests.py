import os

cwd = os.getcwd()
files = [file for file in os.listdir(cwd)
         if file.endswith(".py") and not (file.startswith("runAll") or file.startswith('test_config'))]
for file in files:
    print(f'Running {file}')
    os.system(f"python -m unittest discover -p \"*{file}\"")