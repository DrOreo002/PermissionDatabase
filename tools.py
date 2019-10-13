from datetime import datetime
import string
import fileinput
import sys

dateTimeObj = datetime.now()

PERM_OWNER = 0
PERMISSION = 1
PERM_DESC = 2
PERM_COMMANDS = 3
PERM_DEFAULT_ASIGNMENT = 4

EXPECTED_SIZE = 5

command = sys.argv[1]

# Open the database file
f = open("Database.txt", "r+")
target = open("Backups\\Database Update (" + dateTimeObj.strftime("%d-%b-%Y") + ")" + ".txt", "a+")

# Update the database format
def update_format():
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
    # Close the files
    target.close()
    f.close()
    print("----------- Command executed successfully")
    quit()
    pass

def update_icon():
    print("Icons updating called!")

    icon_data = open("IconData.txt", "w")
    icon_data.truncate()
    icon_data.seek(0)

    last_owner = None
    for line in f.readlines():
        if (line.startswith("#")):
             continue
        dat = line.split("|")
        p_owner = dat[PERM_OWNER]
        if (p_owner != last_owner):
            # New one
            last_owner = p_owner
            material_name = input("[!] Type icon data for plugin " + p_owner + " > ")
            print("         > Material / Icon data selected successfully! (" + material_name + ")")
            icon_data.write(p_owner + "|" + material_name + "\n")
            continue
        # Not new, still continue
        last_owner = dat[PERM_OWNER]
        pass
    # Save and close
    icon_data.flush()
    icon_data.close()

    target.flush()
    target.close()

    # Close only, because we only reads the data
    f.close()

# Main function basically
found = False
if (command.lower() == "-update-format"):
    update_format()
    found = True
    pass
if (command.lower() == "-update-icon"):
    update_icon()
    found = True
    pass

if (not found):
    print("Unknown command!")
    quit()
    pass


