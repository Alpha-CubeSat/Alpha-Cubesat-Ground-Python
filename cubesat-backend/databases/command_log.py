from databases import elastic
from control.control_constants import *
import config
import json

def get_new_processed_cmds(imei, new_cmd_log):
    """
    Compares the command log of the last and most recent normal report to 
    determine the newly processed commands in the time between the last normal
    report and now. 
    """
    last_cmd_log = elastic.get_es_data(
        idx=config.cubesat_db_index, 
        cols=['command_log'],
        query={'term': {'imei': imei}},
        size=1,
        sort=[{"transmit_time": {"order": "desc"}}])
    if last_cmd_log:
        last_cmd_log = last_cmd_log[0]["command_log"]

    new_cmd_log = [item for item in new_cmd_log if item != '0']
    last_cmd_log = [item for item in last_cmd_log if item != '0']

    # If log is empty or it is identical to the last log there are no new commands
    if last_cmd_log == new_cmd_log or new_cmd_log == []:
        return []
    elif last_cmd_log == []:
        return new_cmd_log
    for i in range(1, len(new_cmd_log)):
        if last_cmd_log == new_cmd_log[i:]:
            return new_cmd_log[:i]
        
def get_unprocessed_cmds(imei):
    """
    Returns a list of unprocessed commands from the command log
    """
    unprocessed = []
    opcodes = {DEPLOY, ARM, FIRE, EEPROM_RESET, FRAGMENT_REQUEST, MISSION_OVERRIDE}
    namespace_field = {SFR_OVERRIDE, FAULT}
    with open(f"{config.cmd_log_root_dir}/{imei}.txt", 'r') as file:
        for line in file:
            try:
                data = json.loads(line)
                for command in data.get("commands"):
                    if command["processed"] == "unknown":
                        if command["opcode"] in opcodes:
                            unprocessed.append(command["opcode"])
                        elif command["opcode"] in namespace_field:
                            unprocessed.append(command["namespace"] + "::" + command["field"]) 
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
    return unprocessed[::-1]

def write_command_log(imei, new_processed):
    """
    Writes to the command logs to update the processed field in uplinked 
    commands. 
    """
    changes_made = False
    updated_content = []
    accum = 0
    with open(f"{config.cmd_log_root_dir}/{imei}.txt", 'r') as file:
        for line in file:
            try:
                data = json.loads(line)
                for command in data.get("commands"):
                    if command["processed"] == "unknown" and accum < len(new_processed):
                        command["processed"] = new_processed[accum]
                        changes_made = True
                        accum += 1
                modified_line = json.dumps(data)
                updated_content.append(modified_line)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
    if changes_made:
        with open(f"{config.cmd_log_root_dir}/{imei}.txt", 'w') as file:
            for line in updated_content:
                file.write(line + '\n')


def update_command_log(imei, new_cmd_log):
    """
    Compares the unprocessed commands and newly processed commands and modifies 
    the command logs to reflect newly processed commands. 
    """
    # cmd lists ordered from latest to earliest
    unprocessed = get_unprocessed_cmds(imei)
    new_cmds = get_new_processed_cmds(imei, new_cmd_log)
    i, j = len(unprocessed) - 1, len(new_cmds) - 1

    new_processed = []
    while j >= 0 and i >= 0:
        if new_cmds[j] == unprocessed[i]:
            new_processed.append("processed")
            i, j = i-1, j-1
        else:
            new_processed.append("missing")
            i = i - 1
    write_command_log(imei, new_processed)

        

