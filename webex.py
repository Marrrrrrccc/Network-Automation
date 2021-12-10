import urllib3
import json
import requests

def webexSend():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    host = 'https://api.ciscospark.com'
    teams_path = "/v1/teams"
    rooms_path = "/v1/rooms"
    msg_path = "/v1/messages"
    token = "Bearer YmRmYzg0YWQtZDEzNy00NzJhLWEwMzYtMmYzNTU0MzdjZDc1ZDAwMzMzZDAtMzFh_P0A1_cb5a5b29-3fc8-41df-9e13-7f1e41bb9760"

    teams_url = f"{host}{teams_path}"
    rooms_url = f"{host}{rooms_path}"
    msg_url = f"{host}{msg_path}"

    teams_body = {
        "name": "Support Engineer"
    }

    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }

    teams_get = requests.get(teams_url, headers=headers, verify=False).json()
    teams = teams_get['items']
    for team in teams:
        if team['name'] == 'Support Engineer':
            teamId = team['id']


    rooms_get = requests.get(rooms_url, headers=headers, verify=False).json()
    rooms = rooms_get['items']
    for room in rooms:
        if room['title'] == 'Support Engineer':
            roomId = room['id']


    msg_body = {
        "roomId": roomId,
        "text": "ROUTER 1 UPDATED"
    }
    requests.post(msg_url, headers=headers, data=json.dumps(msg_body), verify=False).json()

webexSend()