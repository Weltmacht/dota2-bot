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
            try:
                response = requests.get(url = f"https://api.opendota.com/api/matches/{match_id}")
                response.raise_for_status()
                data = json.loads(response.text) 
                for player in data.get("players"):
                    print("PSlot: ", player.get("player_slot", 'No slot available'))
                    print("Persona name: ", player.get("personaname", 'No persona name available'))
                    print("Player name: ", player.get("name", 'No name available'))
                    print("Rank: ", player.get("rank_tier", 'No rank available'))
                    print("Position: ", player.get("lane_pos", 'No pos available'))
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