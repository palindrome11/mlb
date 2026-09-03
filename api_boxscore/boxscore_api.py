# api_boxscore/boxscore_api.py
import statsapi
import json
import argparse

def capture_boxscore(game_pk):
    #"""Raw boxscore payload for a single game."""
    return statsapi.get('game_boxscore', {'gamePk': game_pk})

def main():
    parser = argparse.ArgumentParser(description="Fetch a boxscore by gamePk")
    parser.add_argument("game_pk", type=int, help="MLB gamePk identifier")
    args = parser.parse_args()

    game_pk=args.game_pk
    #print(f"game_pk: {args.game_pk}")
    game_boxscore_data = capture_boxscore(args.game_pk)
    #print(json.dumps(game_boxscore_data['teams']['home']['players'], indent=2)[:3000])
    return(game_pk,game_boxscore_data)

if __name__ == "__main__":
  main()