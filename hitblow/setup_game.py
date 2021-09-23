import random
import time
import requests
session = requests.Session()

class Setupgame:

    def __init__(self,ans=None,room_id=1000) -> None:
        self.digits = 5
        self.set_16 = {"0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"}
        if ans is not None:
            self.ans = ans
        else:
            self.ans = self._define_hidden_number()
        self.url = 'https://damp-earth-70561.herokuapp.com'
        self.room_id = room_id
        self.player_id_F = "e6e4dcbe-ec3c-4c2a-b228-67d1acee3c81"
        self.player_id_F2 = "19dfceb3-46be-4d0e-94e2-3aa3333a4442"
        self.player_name = "F"
        self.opponent_name = None
        self.headers = {"content-Type":"application/json"}
        self.my_history = []
        self.opponent_history = []

    def _start_game(self):
        while True:
            url_enter_room = self.url + "/rooms"
            post_data = {"player_id":self.player_id_F, "room_id":self.room_id}
            response_post_enter_room = session.post(url_enter_room,headers=self.headers,json=post_data)
            data = response_post_enter_room.json()
            if data["state"] == 2:
                break
            time.sleep(10)
        self.opponent_name = data["player2"] if data["player1"] == "F" else data["player1"]

    def _define_hidden_number(self) -> str:
        ans_list = random.sample(self.set_16, self.digits)
        ans = "".join(ans_list)
        return ans
    
    def _post_hidden_number(self):
        while True:   
            url_post_hidden_number = self.url + "/rooms/" + self.room_id + "/players/" + self.player_name + "/hidden"
            post_data = {"player_id":self.player_id_F, "hidden_number":self.ans}
            response_post_hidden_number = session.post(url_post_hidden_number,headers=self.headers,json=post_data)
            data = response_post_hidden_number
            if data["selecting"] == "true":
                break

    def _show_result(self,winner,game_end_count) -> None:
        print("------------------------")
        print("show opponent history")
        for k,v in enumerate(self.opponent_history):
            print("{}回目 : {} ".format(k+1,v))
        print("------------------------")
        print("show my history")
        for k,v in enumerate(self.my_history):
            print("{}回目 : {} ".format(k+1,v))

        print("------------------------")
        print("勝者は{}です. {}回で正解しました!".format(winner,game_end_count))
        print("------------------------")




