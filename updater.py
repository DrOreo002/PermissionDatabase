from datetime import datetime
import string
import fileinput

dateTimeObj = datetime.now()

PERM_OWNER = 0
PERMISSION = 1
PERM_DESC = 2
PERM_COMMANDS = 3
PERM_DEFAULT_ASIGNMENT = 4

EXPECTED_SIZE = 5

f = open("Database.txt", "r+")
target = open("Database Update (" + dateTimeObj.strftime("%d-%b-%Y") + ")" + ".txt", "a+")
for line in f.readlines():
    if line.startswith("#"):
        target.write(line)
        continue
    line = line.replace("\n", "")
    x = line.split("|")
    size = len(x)

    # If there's only <pluginName>|<permission>
    if size == 2:
        target.write(x[PERM_OWNER] + "|" + x[PERMISSION] + "|empty|empty|op\n")
        continue
    # If there's only <pluginName>|<permission>|<desc>
    if size == 3: 
        target.write(x[PERM_OWNER] + "|" + x[PERMISSION] + "|" + x[PERM_DESC] + "|empty|op\n")
        continue
    # If there's only <pluginName>|<permission>|<desc>|<commands>    
    if size == 4:
        commandConverted = "<l>" + x[PERM_COMMANDS].replace(",", "<br>") + "<l>"
        target.write(x[PERM_OWNER] + "|" + x[PERMISSION] + "|" + x[PERM_DESC] + "|" + commandConverted + "|op\n")
        continue
    # If complete
    if size == EXPECTED_SIZE:
        commandConverted = x[PERM_COMMANDS]
        if not "<l>" in commandConverted: # This means, not contains
            commandConverted = "<l>" + x[PERM_COMMANDS].replace(",", "<br>") + "<l>"
        target.write(x[PERM_OWNER] + "|" + x[PERMISSION] + "|" + x[PERM_DESC] + "|" + commandConverted + "|" + x[PERM_DEFAULT_ASIGNMENT] + "\n")
        continue
# End of method
target.close()
f.close()
