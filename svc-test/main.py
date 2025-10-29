from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

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
    
    if _previous_known_state != content["map"]["game_state"]:
        _previous_known_state = content["map"]["game_state"]
        if content["map"]["game_state"] == "DOTA_GAMERULES_STATE_HERO_SELECTION":
            pass
        if content["map"]["game_state"] == "DOTA_GAMERULES_STATE_STRATEGY_TIME":
            pass
        if content["map"]["game_state"] == "DOTA_GAMERULES_STATE_SHOWCASE_TIME":
            pass
        if content["map"]["game_state"] == "DOTA_GAMERULES_STATE_GAME_IN_PROGRESS":
            pass
        if content["map"]["game_state"] == "DOTA_GAMERULES_STATE_POST_GAME":
            try:
                response = requests.get(url = f"https://api.opendota.com/api/matches/{match_id}")
                response.raise_for_status()
                data = json.loads(response.text) 
                for player in data["players"]:
                    print("PSlot: ", player["player_slot"])
                    if "personaname" in player:
                        print("Persona name: ", player["personaname"])
                    if "name" in player:
                        print("Player name: ", player["name"])
                    if "rank_tier" in player:
                        print("Rank: ", player["rank_tier"])
                    if "lane_pos" in player:
                        print("Position: ", player["lane_pos"])
                endmatch(content["map"]["win_team"])

            except requests.RequestException as e:
                print(f"OpenDota Request failed: {e}")
                return None
            
    return jsonify(message={"state": "succeeded"}, status=200), 200

def endmatch(win_team):
    global _player_team
    global _previous_known_state

    print("Game winner: ",win_team)
    if _player_team == win_team:
        print("Well it looks like you got carried...")

    # reset match state
    _player_team = ''
    _previous_known_state = ''

if __name__ == "__main__":
    app.run()