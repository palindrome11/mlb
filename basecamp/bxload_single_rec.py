import paths

from api_boxscore.boxscore_api import capture_boxscore

def get_game_box(game_id):
    data=capture_boxscore(game_id)
    return(data)


game_id = 824708
data=get_game_box(game_id)
print(data)