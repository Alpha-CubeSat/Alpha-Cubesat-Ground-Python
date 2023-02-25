from datetime import datetime
import json

"Stores the result of uplinking a command into the command text file logs."
def log_command(command):
    currentMinute = datetime.now().minute
    currentHour = datetime.now().hour
    currentDay = datetime.now().day
    currentMonth = datetime.now().month
    currentYear = datetime.now().year

    time = str(currentHour) + ":" + str(currentMinute)
    date = str(currentMonth) + "/" + str(currentDay) + "/" + str(currentYear)
    writeContent = f"{date},{time},{json.dumps(command)}\n"
    filename = f"commands_{currentYear}.txt"
    file = open(filename, 'a')
    file.write(writeContent)
    file.close()

    # TODO: Add RockBlock response and status of the command

"""Handles a list of commands created by a ground system to send to
the satellite. Authenticates with rockblock web services using credentials
provided in the config file"""
def handle_command(commands):
    print("Processing commands!")
    for command in commands:
        log_command(command)

    # TODO: Add command parsing and Rockblock connection after getting complete
    # list of new commands and new opcodes, any changes to the command format,
    # and setting up the Rockblock to send and receive messages on the portal

