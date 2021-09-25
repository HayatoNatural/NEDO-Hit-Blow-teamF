import random
import time
import requests
session = requests.Session()

class Playgame():
    """16進数5桁のHit&Blow
    手入力で遊ぶモード, 2分探索で遊ぶモード(今後実装)

    :param int digits : 数の桁数
    :param set set_16 : 数に使う16進数の数字の集合
    :param str ans : 自分の答え(相手に当ててもらう数字)
    :param str self.url : API使用の時のURLの共通部分
    :param str room_id : room id(6000~6999)
    :param int room_state : 部屋の状態(1:待機中,2:対戦中,3:対戦終了)
    :param str player_id_F : Fのid
    :param str player_id_F2 : F2のid
    :param str player_name : 名前(F)
    :param str opponent_name : 相手の名前
    :param str now_player : どちらのターンかを表す
    :param dict headers : postするときにjson指定するコマンド
    :param List[dict] my_history : 自分が相手の数当をした時の履歴
    :param List[dict] opponent_history : 相手が自分の数当をした時の履歴
    :param imt count : 何ターンたったか
    :param str num : サーバーにpostする,こちらが予想した相手の数字
    :param int hit : 数字のhit数
    :param int blow : 数字のblow数
    """

    def __init__(self,ans,room_id) -> None:
        """コンストラクタ
        :param str ans : 自分の答え(相手に当ててもらう数字)
        :param str room_id : room id(6000~6999)
        : rtype : None
        : return : なし
        """
        self.digits = 5
        self.set_16 = {"0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"}
        if ans is not None:
            self.ans = ans
        else:
            self.ans = self._define_hidden_number_random()
        self.url = 'https://damp-earth-70561.herokuapp.com'
        self.room_id = room_id
        self.room_state = 1
        self.player_id_F = "e6e4dcbe-ec3c-4c2a-b228-67d1acee3c81"
        self.player_id_F2 = "19dfceb3-46be-4d0e-94e2-3aa3333a4442"
        self.player_name = "F2"
        self.opponent_name = None
        self.now_player = None
        self.headers = {"content-Type":"application/json"}
        self.my_history = None
        self.opponent_history = None
        self.count = 0
        self.list_where_num_is = []
        self.set_ans_num = {}
        self.num = None
        self.hit = None
        self.blow = None


    def _enterroom_and_registerplayer(self):
        """部屋を作成し, 部屋に入り, 相手が来るまで待機
        相手が来たらゲームスタート
        : rtype : None
        : return : なし
        """
        url_enter_room = self.url + "/rooms"
        post_data = {"player_id":self.player_id_F2, "room_id":self.room_id}
        session.post(url_enter_room,headers=self.headers,json=post_data)

        while self.room_state == 1:
            url_get_room = self.url + "/rooms/" + str(self.room_id)    
            result = session.get(url_get_room)
            data = result.json()
            self.room_state = data["state"]
            time.sleep(5)
        self.opponent_name = data["player2"] if data["player1"] == "F" else data["player1"]
        self.now_player = data["player1"]

    def _define_hidden_number_random(self) -> str:
        """相手に当ててもらう答えをつくる
        : rtype : str
        : return : ans
        """
        ans_list = random.sample(self.set_16, self.digits)
        ans = "".join(ans_list)
        return ans
    
    def _post_hidden_number(self):
        """APIを用いてサーバーに自分の答えをポスト
        : rtype : None
        : return : なし
        """
        url_post_hidden_number = self.url + "/rooms/" + self.room_id + "/players/" + self.player_name + "/hidden"
        post_data = {"player_id":self.player_id_F2, "hidden_number":self.ans}
        session.post(url_post_hidden_number,headers=self.headers,json=post_data)


    def _get_table_by_API(self):
        """APIを用いてサーバーから部屋の状態, ターン, 履歴を取得
        : rtype : None
        : return : なし
        """
        url_get_table = self.url + "/rooms/" + str(self.room_id) + "/players/" + self.player_name + "/table"
        result = session.get(url_get_table)
        data = result.json()
        self.room_state = data["state"]
        self.now_player = data["now_player"]
        self.my_history = data["table"]


    def _post_guess_by_API(self):
        """APIを用いてサーバーに予想した相手の数字をポスト
        : rtype : None
        : return : なし
        """
        url_post_guess = self.url + "/rooms/" + str(self.room_id) + "/players/" + self.player_name + "/table/guesses"
        post_data = {"player_id": self.player_id_F2, "guess": self.num} 
        session.post(url_post_guess, headers=self.headers, json=post_data)


    def _play_game_manual(self) -> None:
        """手入力で遊ぶモード
        : rtype : None
        : return : なし
        """
        while self.room_state == 2:
            self._get_table_by_API()
            if self.room_state == 2 and self.now_player == self.player_name:
                print("{}回目の入力です.".format(self.count+1))
                self.num = self._get_your_num()
                self._post_guess_by_API()
                self._get_table_by_API()
                self.hit = self.my_history[-1]["hit"]
                self.blow = self.my_history[-1]["blow"]
                print("!!  {} Hit, {} Blow  !!".format(self.hit,self.blow))
            else:
                time.sleep(5)
                continue
                
            if self.hit == self.digits:
                print("!! 正解です !!")
                break

    def _get_your_num(self) -> str :
        """手入力で遊ぶモードで使用
        予測した相手の数字を入力し, チェック
        条件を満たさないと打ち直し
        : rtype : str
        : return : num
        """
        while True:
            num = input("16進数で5桁の重複しない数字を入力してください ==> ")
            judge = True
            for i in num:
                if i not in self.set_16:
                    judge = False
            if judge == True and len(num) == self.digits and len(set(num)) == self.digits:
                return num
            else:
                print("もう一度入力しなおしてください(16進数, 5桁, 重複なし)")


    def _first_three_times(self) -> None:
        search_list = ["01234","56789","abcde"]
        for i in range(3):
            self._get_table_by_API_1()
            if self.room_state == 2 and self.now_player == self.player_name:
                print("{}回目の入力です.".format(self.count+1))
                self.num = search_list[i]
                self._post_guess_by_API()
                self._get_table_by_API_2()
                self.hit = self.my_history[-1]["hit"]
                self.blow = self.my_history[-1]["blow"]
                self.list_where_num_is.append(self.hit + self.blow)
                print("-----",self.num)
                print("!!  {} Hit, {} Blow  !!".format(self.hit,self.blow))
                if self.hit == self.digits:
                    print("!! 正解です !!")
                    break
            else:
                print("----------from first3 to 5C----------")

    def _identify_5_numbers(self):
        pass

    def _play_game_auto(self):
        self._first_three_times()
        self._identify_5_numbers()


    def run(self, mode="manual") -> None:
        """ 数当てゲーム実行ランナー
        : param str mode : ゲームの実行モード("manual","auto")
        : rtype : None
        : return : なし
        """
        self._enterroom_and_registerplayer()
        self._post_hidden_number()
        if mode == "auto":
            self._play_game_auto()
        else:
            self._play_game_manual()
        self._show_result()


    def _show_result(self) -> None:
        """対戦終了後, お互いの結果を表示
        : rtype : None
        : return : なし
        """
        time.sleep(10)
        url_get_table = self.url + "/rooms/" + str(self.room_id) + "/players/" + self.player_name + "/table"
        result = session.get(url_get_table)
        data = result.json()

        self.my_history = data["table"]
        self.opponent_history = data["opponent_table"]
        print("------------------------")
        print("show opponent history")
        print(self.opponent_history)
        print("------------------------")
        print("show my history")
        print(self.my_history)
        
        winner =data["winner"]
        game_end_count =data["game_end_count"]
        print("------------------------")
        print("勝者は{}です. {}回で正解しました!".format(winner,game_end_count))
        print("------------------------")






