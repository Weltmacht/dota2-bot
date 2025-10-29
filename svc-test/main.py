from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

_player_team: str = ''
_previous_known_state: str = ''

@app.route("/dota2", methods=["POST"])
def process():
    global _player_team
    global _previous_known_state

    content = request.json

    if _player_team == '':
        if "player" in content:
            if "team_name" in content["player"]:
                _player_team = content["player"]["team_name"]

    if 'map' in content:
        print("Game state: ", content["map"]["game_state"])
        match_id = content["map"]["matchid"]
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
                response = requests.get(url = f"https://api.opendota.com/api/matches/{match_id}")
                print(response)
                endmatch(content)

    return jsonify(message={"state": "succeeded"}, status=200), 200

def endmatch(match: dict):
    global _player_team
    global _previous_known_state

    print("Game winner: ", match["map"]["win_team"])
    if match["map"]["win_team"] == match["map"]["win_team"]:
        print("Well it looks like you got carried...")

    # reset match state
    _player_team = ''
    _previous_known_state = ''
    pass

if __name__ == "__main__":
    app.run()