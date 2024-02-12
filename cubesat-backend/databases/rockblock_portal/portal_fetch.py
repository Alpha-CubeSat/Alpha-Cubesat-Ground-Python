import os
from datetime import datetime

import requests
from dotenv import load_dotenv

# Configure Date Here -------------------------------------------------------------------
start_date = datetime(2024, 1, 26, 12, 0, 0)
end_date = datetime(2024, 2, 7, 23, 59, 59)
# ---------------------------------------------------------------------------------------

load_dotenv("portal_fetch.env")

imei_map = {
    "RockBLOCK 202745 (FlatSat)": "300534061570670",
    "RockBLOCK (FlatSat 2)": "300234064326340"
}

# allows remembering of login cookie across requests
session = requests.Session()
api_base = "https://rockblock.rock7.com"

login = session.post(api_base + "/Operations", data={
    "u": os.environ.get('ROCKBLOCK_USER'),
    "p": os.environ.get('ROCKBLOCK_PASS')
})
print("Logged in, cookie is: " + login.cookies.get('R7SESSION'))

# get all telemetry messages between start and end dates
get_message_url = "/RockBlockAdmin/?page=messages&action=getMessages&filterDeviceAssignmentId=&filterDirection=MO&" \
                + f"filterDateFrom={start_date.strftime('%d/%b/%Y %H:%M:%S')}&filterDateTo={end_date.strftime('%d/%b/%Y %H:%M:%S')}"
get_messages = session.post(api_base + get_message_url)
messages = get_messages.json()['messages']
print(f"Retrieved {len(messages)} messages")

# get payload for each message and send to GS
for message in messages:
    # print(message)
    get_message_detail_url = f"/RockBlockAdmin/?page=messages&action=getMessageModalData&sbdId={message['sbdId']}&mtId=0&messageType=MO&deviceAssignmentId={message['deviceAssignmentId']}"
    get_message_details = session.post(api_base + get_message_detail_url)
    message_details = get_message_details.json()['message']
    # print(message_details)

    # update date string format: 06/Feb/2024 14:26:37 => 2024-02-06T14:26:37Z
    transmit_time = datetime.strptime(message_details['dateTime'], '%d/%b/%Y %H:%M:%S')
    gs_data = {
        "data": message_details['data'],
        "transmit_time": transmit_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
        "iridium_latitude": message_details['lat'],
        "iridium_longitude": message_details['lon'],
        "iridium_cep": message_details['iridiumCep'],
        "imei": imei_map[message_details['deviceAssignmentName']],
        "JWT": os.environ.get('JWT')
    }
    print(gs_data)

    # send to GS
    session.post(os.environ.get('API_BASE') + '/api/cubesat/telemetry', json=gs_data)