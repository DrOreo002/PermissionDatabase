import string
import fileinput

PERM_OWNER = 0
PERMISSION = 1
PERM_DESC = 2
PERM_COMMANDS = 3
PERM_DEFAULT_ASIGNMENT = 4

EXPECTED_SIZE = 5

f = open("Database.txt", "r+")
for line in f.readlines():
    if line.startswith("#"):
        f.write(line)
        continue
    line = line.replace("\n", "")
    x = line.split("|")
    size = len(x)

    # If there's only <pluginName>|<permission>
    if size == 2:
        f.write(x[PERM_OWNER] + "|" + x[PERMISSION] + "|empty|empty|op\n")
        continue
    # If there's only <pluginName>|<permission>|<desc>
    if size == 3: 
        f.write(x[PERM_OWNER] + "|" + x[PERMISSION] + "|" + x[PERM_DESC] + "|empty|op\n")
        continue
    # If there's only <pluginName>|<permission>|<desc>|<commands>    
    if size == 4:
        f.write(x[PERM_OWNER] + "|" + x[PERMISSION] + "|" + x[PERM_DESC] + "|" + x[PERM_COMMANDS] + "|op\n")
        continue
f.close()
