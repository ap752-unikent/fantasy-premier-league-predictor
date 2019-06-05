import asyncio
import aiohttp
import pandas as pd
import requests
from datetime import datetime
import dateutil.parser
import csv

X = 3
pre_export_data = []
export_data = []
games_num = 0

def ImportTeamData():
    global team_data
    dataset = pd.read_csv('TeamData.csv', ',', encoding="utf-8")
    team_data = dataset.values
    print(team_data)

def GetOpponentTeamStrength(id):
    for i in range(len(team_data)):
        if(team_data[i][0] == id):
            strength = team_data[i][2]
    
    return strength

async def GetData(
    session: aiohttp.ClientSession,
    id: str,
    element_type: str,
    **kwargs
) -> list:
    global X
    url = f"https://fantasy.premierleague.com/drf/element-summary/{id}"
    print(f"Requesting {url}")
    resp = await session.request('GET', url=url, **kwargs)

    data = await resp.json()
    print(f"Received data for {url}")

    #append player id and element type to data here
    data['id'] = id
    data['element_type'] = element_type

    return data 

def PreparePreExportData(data):

    global games_num
    global X
    global pre_export_data

    ImportTeamData()

    for player_data in data:

        try:
            games = player_data['history']
            element_type = player_data['element_type']
            num_games_returned = len(games)

            for i in range(num_games_returned):
                game_id = games[i]['id']
                #ict_index = games[i]['ict_index']
                #was_home = games[i]['was_home']
                selected = games[i]['selected']
                transfers_balance = games[i]['transfers_balance']
                minutes = 0
                
                if i > 0:
                    minutes = games[i-1]['minutes']

                kickoff_time = games[i]['kickoff_time']
                kickoff_time_obj = dateutil.parser.parse(kickoff_time)
                kickoff_time_obj = kickoff_time_obj.replace(tzinfo=None)
                now = datetime.now()

                if(now > kickoff_time_obj):

                    if num_games_returned - i < 5:
                        break

                    points_next_X = 0
                    team_strength_next_X = 0

                    for ii in range(i, i+X):

                        kickoff_time = games[ii]['kickoff_time']
                        kickoff_time_obj = dateutil.parser.parse(kickoff_time)
                        kickoff_time_obj = kickoff_time_obj.replace(tzinfo=None)
                        now = datetime.now()

                        if(now > kickoff_time_obj):

                            points_next_X += games[ii]['total_points']
                            opponent_team = games[ii]['opponent_team']
                            team_strength_next_X += GetOpponentTeamStrength(opponent_team)

                    avg_points_next_X = float(points_next_X / X)
                    avg_team_strength_next_X = float(team_strength_next_X / X)

                    kickoff_time_obj = dateutil.parser.parse(kickoff_time)
                    kickoff_time_obj = kickoff_time_obj.replace(tzinfo=None)
                    now = datetime.now()

                    games_num += 1

                    game_data = []

                    if element_type == 1:
                        game_data = [game_id, selected, 1, 0, 0, 0, transfers_balance, avg_team_strength_next_X, minutes, avg_points_next_X]
                    elif element_type == 2:
                        game_data = [game_id, selected, 0, 1, 0, 0, transfers_balance, avg_team_strength_next_X, minutes, avg_points_next_X]
                    elif element_type == 3:
                        game_data = [game_id, selected, 0, 0, 1, 0, transfers_balance, avg_team_strength_next_X, minutes, avg_points_next_X]
                    elif element_type == 4:
                        game_data = [game_id, selected, 0, 0, 0, 1, transfers_balance, avg_team_strength_next_X, minutes, avg_points_next_X]

                    #game_data = [game_id, selected, transfers_balance, avg_team_strength_next_X, avg_points_next_X]
                    pre_export_data.append(game_data)
        except Exception as e:
            print(e)


def GetAllPlayers():
    api_query = "https://fantasy.premierleague.com/drf/bootstrap-static"

    r = requests.get(api_query).json()
    players = r['elements']
    num_players_returned = len(players)
    player_details = []

    for i in range(num_players_returned):
        player_detail = {}
        player_detail['id'] = players[i]['id']
        player_detail['element_type'] = players[i]['element_type']
        player_details.append(player_detail)

    return player_details

async def main(players, **kwargs):

    async with aiohttp.ClientSession() as session:
        tasks = []
        for p in players:
            tasks.append(GetData(session=session, id=p['id'], element_type=p['element_type'], **kwargs))

        data = await asyncio.gather(*tasks, return_exceptions=True)

    return data 

def TransformPreExportData():

    for i in range(len(pre_export_data)):

        team_data = pre_export_data[i]
        export_data.append(team_data)

def ExportData(data):
    global export_data

    PreparePreExportData(data)
    TransformPreExportData()

    with open('PlayerData.csv', 'w', newline='') as myfile:
        wr = csv.writer(myfile, dialect='excel')
        headers = ['game_id', 'selected', 'Goalkeeper', 'Defender','Midfielder', 'Attacker', 'transfers_balance', 'avg_team_strength_next_X', 'minutes','points_next_X']
        wr.writerow(headers)
    
        for i in range(len(export_data)):
            wr.writerow(export_data[i])

        print("Dataset successfully created and saved.")

if __name__ == '__main__':
    players = GetAllPlayers()

    api_data = asyncio.run(main(players))  
    ExportData(api_data)
    print(pre_export_data)






