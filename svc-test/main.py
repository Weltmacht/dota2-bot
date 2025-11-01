from flask import Flask, request, jsonify
import logging
import requests
import json
import time

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.disabled = True

_player_team: str = ''
_previous_known_state: str = ''

@app.route("/dota2", methods=["POST"])
def process():
    global _player_team
    global _previous_known_state

    content = request.json

    match_id = content.get("map", {}).get("matchid")

    if _player_team == '':
        _player_team = content.get("player", {}).get("team_name", '')
    
    if _previous_known_state != content.get("map", {}).get("game_state"):
        _previous_known_state = content.get("map", {}).get("game_state")
        if content.get("map", {}).get("game_state") == "DOTA_GAMERULES_STATE_HERO_SELECTION":
            pass
        if content.get("map", {}).get("game_state") == "DOTA_GAMERULES_STATE_STRATEGY_TIME":
            pass
        if content.get("map", {}).get("game_state") == "DOTA_GAMERULES_STATE_SHOWCASE_TIME":
            pass
        if content.get("map", {}).get("game_state") == "DOTA_GAMERULES_STATE_GAME_IN_PROGRESS":
            pass
        if content.get("map", {}).get("game_state") == "DOTA_GAMERULES_STATE_POST_GAME":
            match_results(match_id)
            endmatch(content["map"]["win_team"])

    return jsonify(message={"state": "succeeded"}, status=200), 200

def match_results(match_id):
    try:
        # 
        i = 0
        while(True):
            time.sleep(5)  # Random sleep time to check for DOTA2 response
            response = requests.get(url = f"https://api.opendota.com/api/matches/{match_id}")
            if response.status_code != 404 or response.status_code != 200:
                response.raise_for_status()
                break
            i = i + 1
            print(f"Waiting for match results, attempt: {i}/5")
            if i >= 5:
                print("No match results found!")
                return jsonify(message={"state": "succeeded"}, status=200), 200
        
        # Request to have replay parsed
        jobid = json.loads(requests.post(url = f"https://api.opendota.com/api/request/{match_id}").text)["job"]["jobId"]
        time.sleep(30)  # Initial sleep time for replay parse
        
        # Loop to wait for parsing on OpenDota to finish
        i = 0
        while(True):
            time.sleep(5)
            jobresponse = requests.get(url = f"https://api.opendota.com/api/request/{jobid}")
            if jobresponse.status_code != 404 or jobresponse.status_code != 200:
                jobresponse.raise_for_status()
                break
            i = i + 1
            print(f"Waiting for match replay parsing, attempt: {i}/10")
            if i >= 10:
                print("Replay parsing still on-going!")
                return jsonify(message={"state": "succeeded"}, status=200), 200
    except requests.RequestException as e:
        print(f"OpenDota Request failed: {e}")
        return jsonify(message={"state": "succeeded"}, status=200), 200

    data = json.loads(response.text) 
    for player in data.get("players"):
        print("PSlot: ", player.get("player_slot", 'No slot available'))
        print("Persona name: ", player.get("personaname", 'No persona name available'))
        print("Player name: ", player.get("name", 'No name available'))
        print("Rank: ", player.get("rank_tier", 'No rank available'))
        print("Account ID: ", player.get("account_id", "No account id available"))
        # print("Position: ", player.get("lane_pos", 'No pos available'))

def endmatch(win_team):
    global _player_team
    global _previous_known_state

    print("Game winner: ", win_team)
    if _player_team == win_team:
        print("Well it looks like you got carried...")

    # reset match state
    _player_team = ''
    _previous_known_state = ''

if __name__ == "__main__":
    app.run()