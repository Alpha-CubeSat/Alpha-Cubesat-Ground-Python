from datetime import datetime
import control.control_protocol as cp
import json

FLAG_LENGTH = 2

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

"""Helper function that translates the decimal number n into an all uppercase
hexidecimal string without '0x' header, then pads hexadecimal string with '0's 
at the beginning until it has the length of FLAG_LENGTH."""
def format_flag(n):
    flag = (hex(n)[2:]).upper()
    while len(flag) < FLAG_LENGTH:
        flag = "0" + flag
    return flag

"""Handles a list of commands created by a ground system to send to
the satellite. Authenticates with rockblock web services using credentials
provided in the config file"""
def handle_command(commands):
    print("Processing commands!")
    uplink = ""
    for command in commands:
        log_command(command)
        uplink += cp.parse_command(command)

    uplink += format_flag(0) + format_flag(250)
    with open('./control/rockblock_config.json') as f:
        rockblock_config = json.load(f)
    cp.send_uplink(rockblock_config['imei'], rockblock_config['user'], rockblock_config['password'], uplink)