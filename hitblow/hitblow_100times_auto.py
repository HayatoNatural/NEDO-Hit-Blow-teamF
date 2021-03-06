# coding : UTF-8
"""
File Name: setup_and_play_game.py
Description: Hit&Blowの主要なクラス
Created on october 7,2021
Created by Hayato Mori, Kaito Isshiki, Chao Wang
"""
import random
import time
import itertools
import argparse
import requests
session = requests.Session()


class Playgame():
    """16進数5桁のHit&Blow
    手入力で遊ぶモード, 自動探索で遊ぶモード(今後実装)

    :param int digits : 数の桁数
    :param Tuple Tuple_16 : 数に使う16進数の数字のタプル
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

    def __init__(self,ans=None,room_id=6000) -> None:
        """コンストラクタ
        :param str ans : 自分の答え(相手に当ててもらう数字)
        :param str room_id : room id(6000~6999)
        : rtype : None
        : return : なし
        """
        self.digits = 5
        self.Tuple_16 = ("0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f")
        if ans is not None:
            self.ans = ans
        else:
            self.ans = self._define_hidden_number_random()
        self.url = 'https://damp-earth-70561.herokuapp.com'
        self.room_id = str(room_id)
        self.room_state = 1
        self.player_id_F = "e6e4dcbe-ec3c-4c2a-b228-67d1acee3c81"
        self.player_id_F2 = "19dfceb3-46be-4d0e-94e2-3aa3333a4442"
        self.player_name = "F"
        self.opponent_name = None
        self.now_player = None
        self.headers = {"content-Type":"application/json"}
        self.list_num_place = []
        self.list_possible_ans_combination = []
        self.list_ans_combination = []
        self.list_possible_ans = []
        self.num = None
        self.hit = None
        self.blow = None
        self.my_history = None
        self.opponent_history = None
        self.count = 0
        self.winner = None

    def _define_hidden_number_random(self) -> str:
        """相手に当ててもらう答えをつくる
        : rtype : str
        : return : ans
        """
        ans_list = random.sample(self.Tuple_16, self.digits)
        ans = "".join(ans_list)
        return ans


    def _enterroom_and_registerplayer(self):
        """部屋を作成し, 部屋に入り, 相手が来るまで待機
        3秒ごとに相手が来ているか確認して,相手が来たらゲームスタート
        : rtype : None
        : return : なし
        """
        url_enter_room = self.url + "/rooms"
        post_data = {"player_id":self.player_id_F, "room_id":self.room_id}
        session.post(url_enter_room,headers=self.headers,json=post_data)

        while self.room_state == 1:
            url_get_room = self.url + "/rooms/" + str(self.room_id)
            result = session.get(url_get_room)
            data = result.json()
            self.room_state = data["state"]
            time.sleep(3)
        self.opponent_name = data["player2"] if data["player1"] == "F" else data["player1"]
        self.now_player = data["player1"]


    def _post_hidden_number(self):
        """APIを用いてサーバーに自分の答えをポスト(初回のみ)
        : rtype : None
        : return : なし
        """
        url_post_hidden_number = self.url + "/rooms/" + self.room_id + "/players/" + self.player_name + "/hidden"
        post_data = {"player_id":self.player_id_F, "hidden_number":self.ans}
        session.post(url_post_hidden_number,headers=self.headers,json=post_data)


    def _get_table_by_API(self):
        """APIを用いてサーバーから部屋の状態,ターン,履歴を取得(ループで何回も使用)
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
        """APIを用いてサーバーに予想した相手の数字(self.num)をポスト
        : rtype : None
        : return : なし
        """
        url_post_guess = self.url + "/rooms/" + str(self.room_id) + "/players/" + self.player_name + "/table/guesses"
        post_data = {"player_id": self.player_id_F, "guess": self.num}
        session.post(url_post_guess, headers=self.headers, json=post_data)


    # def _play_game_manual(self) -> None:
    #     """手入力で遊ぶモード
    #     対戦続行中で,自分のターンのとき, 推測した値をサーバーにpost
    #     5秒ごとに自分のターンが来たかを確認

    #     : rtype : None
    #     : return : なし
    #     """
    #     while self.room_state == 2:
    #         self._get_table_by_API()
    #         if self.room_state == 2 and self.now_player == self.player_name:
    #             print("{}回目の入力です.".format(self.count+1))
    #             self.num = self._get_your_num()
    #             self._post_guess_by_API()
    #             self._get_table_by_API()
    #             self.hit = self.my_history[-1]["hit"]
    #             self.blow = self.my_history[-1]["blow"]
    #             print("-----"+self.num + "  {} Hit, {} Blow  !!".format(self.hit,self.blow))
    #         else:
    #             time.sleep(5)
    #             continue

    #         if self.room_state == 3:
    #             break

    # def _get_your_num(self) -> str :
    #     """手入力で遊ぶモードで使用
    #     予測した相手の数字を入力し, チェック
    #     条件を満たさないと打ち直し
    #     : rtype : str
    #     : return : num
    #     """
    #     while True:
    #         num = input("16進数で5桁の重複しない数字を入力してください ==> ")
    #         judge = True
    #         for i in num:
    #             if i not in self.Tuple_16:
    #                 judge = False
    #         if judge == True and len(num) == self.digits and len(set(num)) == self.digits:
    #             return num
    #         else:
    #             print("もう一度入力しなおしてください(16進数, 5桁, 重複なし)")


    def _first_2_times(self) -> None:
        """自動数当てモードで最初に行う, 答えとなる数字がどのグループに何個あるのか特定
        1秒ごとにget_tableで状態を確認し,
        対戦続行中で,自分のターンのとき, 1,2回目に01234,56789を選んでself.numに格納
        post_guessし, 帰ってきたhit,blowの和をlist_ans_numに格納
        remove_impossible_combinationを行う
        自分のターンで無かったら, 1秒待機
        試合終了だったらループを抜ける
        : rtype : None
        : return : なし
        """
        search_list = ["01234","56789"]
        while True:
            self._get_table_by_API()
            if self.room_state == 2 and self.now_player == self.player_name and self.count != 2:
                print("{}回目の入力です.".format(self.count+1))
                self.num = search_list[self.count]
                self.count += 1
                self._post_guess_by_API()
                self._get_table_by_API()
                self.hit = self.my_history[-1]["hit"]
                self.blow = self.my_history[-1]["blow"]
                self.list_num_place.append(self.hit + self.blow)
                print("-----",self.num)
                print("!!  {} Hit, {} Blow  !!".format(self.hit,self.blow))
            if self.count == 3 or self.room_state == 3:
                break
            else:
                time.sleep(0.5)
                continue


    def _make_list_possible_ans_combination(self) -> None:
        """自動数当てモードで2番目に行う
        最初の3回で作ったlist_ans_numから, 答えの5数字の"組み合わせ"の候補を全て洗い出し,
        list_possible_ans_combinationに格納
        : rtype : None
        : return : なし
        """
        for i in itertools.combinations("01234", self.list_num_place[0]):
            for j in itertools.combinations("56789", self.list_num_place[1]):
                for k in itertools.combinations("abcdef", self.digits-sum(self.list_num_place)):
                    n = "".join(i+j+k)
                    self.list_possible_ans_combination.append(n)

    def _remove_impossible_combination(self):
        """自動数当てモードの3番目で使用
        そのターンに質問で帰ってきたhit,blowの値を保存し, list_possible_ans_combinationの解の候補のiのうち
        self.numとiでhit,blowの和が一致しないものは答えの"組み合わせ"の候補としてありえないので候補から削除
        こうしてlist_possible_ans_combinationの中身を削っていく
        : rtype : None
        : return : なし
        """
        hb = self.hit + self.blow
        for i in self.list_possible_ans_combination[:]:
            self._check_hit_blow(self.num,i)
            if self.hit + self.blow != hb:
                self.list_possible_ans_combination.remove(i)


    def _remove_impossible_permutation(self):
        """自動数当てモードの3番目で使用
        そのターンに質問で帰ってきたhitの値を保存し, list_possible_ansの解の候補のjのうち
        self.numとjでhitが一致しないものは答えの"順列"の候補としてありえないので候補から削除
        こうしてlist_possible_ansの中身を削っていく
        : rtype : None
        : return : なし
        """
        hit = self.hit
        for i in self.list_possible_ans[:]:
            self._check_hit_blow(self.num,i)
            if self.hit != hit:
                self.list_possible_ans.remove(i)


    def _check_hit_blow(self,num,ans) -> None:
        """自動数当てモードの2つのremove関数内で使用
        2つの引数を入力し, その2数のhit,blowを計算してself.hit, self.blowに格納
        : rtype : None
        : return : なし
        """
        self.hit = 0
        self.blow = 0
        for i in range(self.digits):
            if num[i] == ans[i]:
                self.hit += 1
            else:
                if num[i] in ans:
                    self.blow += 1


    def _identify_number(self) -> None:
        """自動数当てモードで3番目に行う(1番のメイン部分)
        1秒ごとにget_tableで状態を確認し,
        対戦続行中で,自分のターンのとき, list_ans_num_combinationの中からランダムで質問する数字を選んでself.numに格納
        post_guessし, 帰ってきたhit,blowをprintし, remove_impossible_combinationを行う
        hit+blow = 5の(組み合わせが特定出来た)ときは, まずその結果からあり得る数字の順列120通りのlist_possible_ansを作成
        次にそのターンのhit,blowからあり得ないものを削除し, 順列を考える次の関数(後述)に移る
        自分のターンで無かったら, 1秒待機
        試合終了だったらループを抜ける
        : rtype : None
        : return : なし
        """
        print("----------from first3 to 5C----------")
        while True:
            self._get_table_by_API()
            if self.room_state == 2 and self.now_player == self.player_name:
                print("{}回目の入力です, 組み合わせの候補は{}通りです.".format(self.count+1,len(self.list_possible_ans_combination)))
                self.count += 1
                self.num = random.choice(self.list_possible_ans_combination)
                self._post_guess_by_API()
                self._get_table_by_API()
                self.hit = self.my_history[-1]["hit"]
                self.blow = self.my_history[-1]["blow"]
                print("-----",self.num)
                print("!!  {} Hit, {} Blow  !!".format(self.hit,self.blow))
                if self.hit + self.blow == self.digits:
                    self.list_ans_combination = [i for i in self.num]
                    for i in itertools.permutations(self.list_ans_combination,5):
                        m = "".join(i)
                        self.list_possible_ans.append(m)
                    print("----------from 5C to 5P----------")
                    self._remove_impossible_permutation()
                    self._identify_permutation()
                    break
                else:
                    self._remove_impossible_combination()
            if self.room_state == 3 :
                break
            else:
                time.sleep(0.5)
                continue


    def _identify_permutation(self) -> None:
        """自動数当てモードの3番目で使用
        1秒ごとにget_tableで状態を確認し,
        対戦続行中で,自分のターンのとき, list_ans_numの中からランダムで質問する数字を選んでself.numに格納
        post_guessし, 帰ってきたhitをprintし, remove_impossible_ansを行う
        自分のターンで無かったら, 1秒待機
        試合終了だったらループを抜ける
        : rtype : None
        : return : なし
        """
        while True:
            self._get_table_by_API()
            if self.room_state == 2 and self.now_player == self.player_name:
                print("{}回目の入力です, 順列の候補は{}通りです.".format(self.count+1,len(self.list_possible_ans)))
                self.count += 1
                self.num = random.choice(self.list_possible_ans)
                self._post_guess_by_API()
                self._get_table_by_API()
                self.hit = self.my_history[-1]["hit"]
                self.blow = self.my_history[-1]["blow"]
                print("-----",self.num)
                print("!!  {} Hit, {} Blow  !!".format(self.hit,self.blow))
                self._remove_impossible_permutation()
            if self.room_state == 3 :
                break
            else:
                time.sleep(0.5)
                continue


    def _show_result_vscode(self) -> None:
        """対戦終了後, お互いの結果を表示(vscode上に表示する分)
        : rtype : None
        : return : なし
        """
        time.sleep(3)
        print("--------------------")
        print("対戦終了です.")
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

        self.winner = data["winner"]
        print("------------------------")
        print("勝者は{}です. {}回で正解しました!".format(self.winner, self.count))
        print("終了ターンの解答 : {}".format(self.num))
        print("------------------------")

    def run(self) -> None:
        """ 自動数当てゲーム実行ランナー
        対戦中の表示を出してから部屋を作成して答えをポストして対戦開始, 終わったら対戦終了と結果の表示
        : rtype : None
        : return : なし
        """
        self._enterroom_and_registerplayer()
        self._post_hidden_number()
        self._first_2_times()
        self._make_list_possible_ans_combination()
        self._identify_number()
        self._show_result_vscode()


def get_parser() -> argparse.Namespace:
    """コマンドライン引数を解析したものを持つ
    :rtype : argparse.Namespace
    :return : コマンド値
    """
    parser = argparse.ArgumentParser(description="Hit&Blow, 数当てゲーム")
    parser.add_argument("--ans",default=None)
    parser.add_argument("--roomid",default="6100")

    args = parser.parse_args()
    return args

def main() -> None:
    """Hit&Blowのメイン
    パーサーで指定したroom_idから昇順に100個の部屋に入って自動対戦する
    """

    args = get_parser()
    room_id = args.roomid
    room_id_int = int(room_id)
    ans= args.ans

    for i in range(100):
        room_id = str(room_id_int+i)
        if ans is not None:
            runner = Playgame(ans=ans,room_id=room_id)
        else:
            runner = Playgame(room_id=room_id)
        runner.run()

if __name__ == "__main__":
    main()
