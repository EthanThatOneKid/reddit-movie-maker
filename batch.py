# Dependencies
import sys, subprocess

# Main Process

## Reading Batch Config
print("Reading Batch Config")
try:
    batch_config_path = sys.argv[1]
except:
    batch_config_path = "static/batch_config.txt"
batch_document = open(batch_config_path, "r", encoding="utf8").read()
commands = []
for post in batch_document.split("\n"):
    if len(post) > 0:
        command = "py main.py {}".format(post)
        commands.append(command)
command = " & ".join(commands)

## Executing Batch Command
print("Executing Batch Command")
print("Creating {} videos".format(len(commands)))
print("Command: {}".format(command))
subprocess.call(command)

## All Done
print("All Done")
exit()
