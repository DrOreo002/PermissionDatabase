# Python3 program that contains useful tools
# to manage permission database, currently for offline usage only
# this will be removed later if the website is up
# 
# 
# Made by DrOreo002
from datetime import datetime
from colorama import Fore
from colorama import Style
from colorama import init

import string
import fileinput
import signal
import sys
import re

init() # Init the colorama

dateTimeObj = datetime.now()

PERM_OWNER = 0
PERMISSION = 1
PERM_DESC = 2
PERM_COMMANDS = 3
PERM_DEFAULT_ASIGNMENT = 4

EXPECTED_SIZE = 5

INFO_TEXT = Fore.RESET + Fore.GREEN + "[!]" + Fore.WHITE + " "

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

# Update the inventory icon with Materials.
def update_icon():
    print("Icons updating called!")

    icon_data = open("IconData.txt", "r+")
    loaded_data = [None]
    last_owner = None

    for line in icon_data.readlines():
        loaded_data.append(line.split("|")[0]) # Append the plugin name

    for line in f.readlines():
        if (line.startswith("#")):
             continue
        dat = line.split("|")
        p_owner = dat[PERM_OWNER]

        if p_owner in loaded_data:
            continue # Ignore this one

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

# Basically will update the player head texture
# dependending the value specified
def update_player_head():
    p_heads = {}
    updated_heads = {}
    line_number = 0
    icon_data = open("IconData.txt", "r+")
    for line in icon_data.readlines():
        if "PLAYER_HEAD" in line:
            if not len(line.split("|")) > 2:
                # This rstrip will remove the \n from the line
                p_heads[line.rstrip()] = line_number # Add to hashmap 
        line_number += 1

    if len(p_heads) == 0:
        print(INFO_TEXT + "No update-able heads found!")
        quit(0)
        pass

    for key in list(p_heads.keys()):
        print(INFO_TEXT + "Found PLAYER_HEAD on line " + Fore.RED + str(p_heads.get(key)) + Fore.WHITE + " is > " + Fore.GREEN + key + Fore.RESET)

    print(Fore.MAGENTA + "------------------------------------")

    allData = True
    for key in list(p_heads.keys()):
        print(INFO_TEXT + "Please type texture for " + Fore.RED + key + Fore.WHITE + " (Type SAVE to quit and save)")
        texture = input("       > ")
        if texture == "SAVE":
            allData = False
            for key in list(updated_heads.keys()):
                print(INFO_TEXT + "Saving " + Fore.RED + key + Fore.WHITE + " into line number " + str(updated_heads.get(key)))
            break

        l_number = p_heads.get(key)
        updated_heads[key + "|" + texture] = l_number

    if allData:
        for key in list(updated_heads.keys()):
            print(INFO_TEXT + "Saving " + Fore.RED + key + Fore.WHITE + " into line number " + str(updated_heads.get(key)))

    f_data = []

    icon_data.seek(0)
    line_number = 0

    for line in icon_data.readlines():
        for key, val in updated_heads.items():
            # There's a change. We use different assignment then
            if line.split("|")[0] == key.split("|")[0]:
                f_data.append(key + "\n")
                line_number += 1
                break
            else:
                f_data.append(line)
                line_number += 1
                break
        line_number += 1

    # Replace the lines
    icon_data.close()
    open("IconData.txt", "w").close(); # Clear the file!
    icon_data = open("IconData.txt", "r+")

    # Write to file
    icon_data.writelines(f_data)
    icon_data.flush()
    icon_data.close()
    print(Fore.MAGENTA + "------------------------------------")
    print(INFO_TEXT + "Data saved successfully...")
    pass

# Show data information
def show_information():
    version = "UNKNOWN"
    perm_owners = []
    perm_icon = []

    icon_data = open("IconData.txt", "r+")

    for line in f.readlines():
        pl_name = line.split("|")[0]
        if pl_name in perm_owners:
            continue
        perm_owners.append(pl_name)

    for line in icon_data.readlines():
        pl_name = line.split("|")[0]
        if pl_name in perm_icon:
            continue
        perm_icon.append(pl_name)

    f.seek(0)
    icon_data.seek(0)

    for line in f.readlines():
        if "Version" in line and line.startswith("#"):
            version = line.split(" ")[2]
            break

    f.seek(0) # Reset to beginning
    data_size = sum(1 for l in f.readlines())
    perm_owners_size = sum(1 for p in perm_owners)
    icon_size = sum(1 for icon in perm_icon)

    print(INFO_TEXT + "Data information for database version " + Fore.RED + "v" +  version + Fore.RESET, end = '')
    print("-------")
    print(INFO_TEXT + "Data size > " + Fore.RED + str(data_size) + " lines" + Fore.RESET)
    print(INFO_TEXT + "Loaded permission owner > " + Fore.RED + str(perm_owners_size))
    print(INFO_TEXT + "Loaded permission owner > " + Fore.RED + str(perm_owners_size) + Fore.RESET)
    print("-------")
    print(INFO_TEXT + "End of data information. More will be given in the future" + Fore.RESET)

    # End
    f.close()
    target.close()
    icon_data.close()
    pass

# Will check for duplicated icons
def check_duplicated_icon():
    print("Checking for duplicated icons...")

    icon_data = open("IconData.txt", "r+")
    loaded_data = {}
    last_owner = None

    for line in icon_data.readlines():
        line = line.rstrip()
        dat = line.split("|")
        if (dat[1] in loaded_data):
            loaded_data[dat[1]] = loaded_data.get(dat[1]) + 1
        else:
            loaded_data[dat[1]] = 1

    for data in loaded_data:
        if loaded_data[data] > 2:
            print(INFO_TEXT + data + " has in total of " + Fore.RED + str(loaded_data[data]) + Fore.WHITE + " duplicates")

    # Save and close
    icon_data.flush()
    icon_data.close()

    target.flush()
    target.close()

    # Close only, because we only reads the data
    f.close()

def validate_icon():
    print(INFO_TEXT + "Checking for invalid icons!")

    icon_data = open("IconData.txt", "r+")
    invalid = []

    for line in icon_data.readlines():
        dat = line.split("|")[0]
        if not re.match("^[A-Za-z0-9_-]*$", dat):
            invalid.append(dat)

    if len(invalid) != 0:
        print(INFO_TEXT + "Found " + str(len(invalid)) + " invalid icons!");
        for s in invalid:
            print("     " + Fore.RED + "[!]" + Fore.WHITE + " " + s)
    else:
        print(INFO_TEXT + "No invalid icons found!");

    icon_data.close()

def check_duplicated_icon_name():
    print(INFO_TEXT + "Checking for duplicated icon name...")

    icon_data = open("IconData.txt", "r+")
    loaded_data = {}

    for line in icon_data.readlines():
        dat = line.split("|")
        if dat[0] in loaded_data.keys():
            loaded_data[dat[0]] = loaded_data.get(dat[0]) + 1
        else:
            loaded_data[dat[0]] = 1

    hasDuplicate = False

    for key, val in loaded_data.items():
        if val > 1:
            hasDuplicate = True
            print(Fore.WHITE + "     > Found duplicate for data " + key + Fore.GREEN + "(" + str(val) + ")")

    if not hasDuplicate:
        print(INFO_TEXT + "No duplicated icon name found. Hooray!")

    # Save and close
    icon_data.flush()
    icon_data.close()

    target.flush()
    target.close()

    # Close only, because we only reads the data
    f.close()

# Quit handler
def handler(signum, frame):
    print(" ")
    print(INFO_TEXT + Fore.RED + "Force closing the program...")
    quit()
    pass

signal.signal(signal.SIGINT, handler)

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
if (command.lower() == "-check-for-duplicated-icon"):
    check_duplicated_icon()
    found = True
    pass
if (command.lower() == "-check-for-duplicated-icon-name"):
    check_duplicated_icon_name()
    found = True
    pass
if (command.lower() == "-info"):
    show_information()
    found = True
    pass
if (command.lower() == "-update-player-heads"):
    update_player_head()
    found = True
    pass
if (command.lower() == "-validate-icons"):
    validate_icon()
    found = True
    pass

if (not found):
    print("Unknown command!")
    quit()
    pass


