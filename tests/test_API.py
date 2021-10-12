# coding : UTF-8
"""
File Name: test_API.py
Description: pytest/requests
Created on october 6,2021
Created by  Chao Wang, Hayato Mori, Kaito Isshiki
"""

import requests
import json


# Run test
def test_player1() ->None:
        # [GET] Get Table(F2)
        room_id = 6010
        url= 'https://damp-earth-70561.herokuapp.com'
        player_name = "F2"
        url_get_table = url + "/rooms/" + str(room_id) + "/players/" + player_name + "/table"
        result = requests.get(url_get_table)
        data = result.json()
        last_table=data["table"][-1]
        # Judge whether http requests succeed and the game ends
        assert result.status_code==200
        assert data["state"] == 3
        assert data["now_player"] == "F"
        assert last_table["hit"]==5
        assert last_table["blow"]==0

def test_player2() ->None:
        # [GET] Get Table(F)
        room_id = 6010
        url= 'https://damp-earth-70561.herokuapp.com'
        player_name = "F"
        url_get_table = url + "/rooms/" + str(room_id) + "/players/" + player_name + "/table"
        result = requests.get(url_get_table)
        data = result.json()
        last_opponent_table=data["opponent_table"][-1]
        # Judge whether http requests succeed and the game ends
        assert result.status_code==200
        assert data["state"] == 3
        assert data["now_player"] == "F"
        assert last_opponent_table["hit"]==5
        assert last_opponent_table["blow"]==0
