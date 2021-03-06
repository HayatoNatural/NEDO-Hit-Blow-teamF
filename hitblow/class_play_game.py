# coding : UTF-8
"""
File Name: class_play_game.py
Description: Hit&Blowの自動通信対戦の主要なクラス
Created on october 13,2021
Created by Hayato Mori, Kaito Isshiki, Chao Wang
"""
import random
import time
import itertools
import streamlit as st
import requests
# st.set_page_config(layout="wide")
import pygame
from PIL import Image
session = requests.Session()

def initialize_streamlit() ->None:
    """クラスを定義する前にweb上で画面を出しておく
    状態量として, 試合数, 経験値, レベル, 連勝数を定義し, 初期化しておく(マジックコマンド的な)
    : rtype : None
    : return : なし
    """
    st.session_state.col1,st.session_state.col2 = st.columns([4,1])
    st.session_state.col4,st.session_state.space,st.session_state.col6 = st.columns([7,1,4])

    st.session_state.col1.title("Welcome to Hit&Blow Game！16進数5桁の数字を当てよう！")
    st.session_state.col1.subheader("対戦すると経験値がもらえるよ. 経験値は当てた回数や連勝数に応じて増えるぞ！")
    st.session_state.col1.subheader("経験値が貯まるとレベルアップだ！いずれはキャラが進化するかも‥？")
    # st.markdown("**_524160_**通りから相手の数字を当ててレベルアップしよう！")
    if 'game_count' not in st.session_state:
        st.session_state.game_count = 0
    if 'exp' not in st.session_state:
        st.session_state.exp = 0
    if 'level' not in st.session_state:
        st.session_state.level = 1
    if 'win_in_a_row' not in st.session_state:
        st.session_state.win_in_a_row = 0
    name = st.session_state.col4.selectbox("キャラクターを選んでね",["ジャック","クリス","フローラ","ドロシー"])
    st.session_state.chara_name = name
    pygame.mixer.init()    # 初期設定
    sound_waiting = pygame.mixer.Sound('voice/'+st.session_state.chara_name+'/waiting.wav')     # 音楽ファイルの読み込み
    sound_waiting.play()
    pic_url1 = "picture/"+name+"-1.jpg"
    pic_url2 = "picture/"+name+"-2.jpg"
    if st.session_state.level < 20:
        image = Image.open(pic_url1)
        st.session_state.col4.image(image)
    else:
        image = Image.open(pic_url2)
        st.session_state.col4.image(image)

class Playgame():
    """16進数5桁のHit&Blow　自動通信対戦の数当てモード

    :param int digits : 数の桁数
    :param set Tuple_16 : 数に使う16進数の数字の集合
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
    :param int volume:音量(0～1で変更)
    :param int remaining_exp_level:レベルアップに必要な経験値を保存する用
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
        self.volume = 0.3
        self.remaining_exp_level = 0

    def _define_hidden_number_random(self) -> str:
        """相手に当ててもらう答えをつくる
        : rtype : str
        : return : ans
        """
        ans_list = random.sample(self.Tuple_16, self.digits)
        ans = "".join(ans_list)
        return ans

    def _play_song(self,num:int, title) -> None:
        """音楽再生
        :param int num:再生回数(-1で無限ループ，これを使って止めたいときにstopするのが良いかと)
        :param int playtime:再生時間(基本-1で無限ループしてるので、使わない．デフォルト値Noneで良い)
        :param str title:bgmフォルダ内にあるmp3ファイルを再生
        : rtype : None
        : return : なし
        """
        pygame.mixer.init()    # 初期設定
        pygame.mixer.music.load(title)     # 音楽ファイルの読み込み
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play(num)              # 音楽の再生回数(1回)

    def _music_stop(self) -> None:
        """再生中の音楽停止
        : rtype : None
        : return : なし
        """
        pygame.mixer.music.stop()               # 再生の終了

    def _sound_play(self,num:int, title):
        pygame.mixer.init()    # 初期設定
        sound = pygame.mixer.Sound(title)     # 音楽ファイルの読み込み
        sound.set_volume(self.volume)
        sound.play()


    def _get_table_by_API(self) -> None:
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

    def _post_guess_by_API(self) -> None:
        """APIを用いてサーバーに予想した相手の数字(self.num)をポスト
        : rtype : None
        : return : なし
        """
        url_post_guess = self.url + "/rooms/" + str(self.room_id) + "/players/" + self.player_name + "/table/guesses"
        post_data = {"player_id": self.player_id_F, "guess": self.num}
        session.post(url_post_guess, headers=self.headers, json=post_data)


    def _enterroom_and_registerplayer(self) -> None:
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
        self._music_stop()
        self._sound_play(num = 1, title = 'voice/'+st.session_state.chara_name+'/game_start.wav')
        self._play_song(num = 1,title = "bgm/game_start.wav")
        time.sleep(3)
        self._play_song(num = -1,title = "bgm/Battle.wav")
        self.opponent_name = data["player2"] if data["player1"] == "F" else data["player1"]
        self.now_player = data["player1"]


    def _post_hidden_number(self) -> None:
        """APIを用いてサーバーに自分の答えをポスト(初回のみ)
        : rtype : None
        : return : なし
        """
        url_post_hidden_number = self.url + "/rooms/" + self.room_id + "/players/" + self.player_name + "/hidden"
        post_data = {"player_id":self.player_id_F, "hidden_number":self.ans}
        session.post(url_post_hidden_number,headers=self.headers,json=post_data)


    def _first_3_times(self) -> None:
        """進化前,最初に行う, 答えとなる数字がどのグループに何個あるのか特定
        1秒ごとにget_tableで状態を確認し,
        対戦続行中で,自分のターンのとき, 1,2,3回目に01234,56789,abcdeを選んでself.numに格納
        post_guessし, 帰ってきたhit,blowの和をlist_ans_numに格納
        remove_impossible_combinationを行う
        自分のターンで無かったら, 1秒待機
        試合終了だったらループを抜ける
        : rtype : None
        : return : なし
        """
        search_list = ["01234","56789","abcde"]
        while True:
            self._get_table_by_API()
            if self.room_state == 2 and self.now_player == self.player_name and self.count != 3:
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

    def _make_list_possible_ans_combination_3(self) -> None:
        """進化前,2番目に行う
        最初の3回で作ったlist_ans_numから, 答えの5数字の"組み合わせ"の候補を全て洗い出し,
        list_possible_ans_combinationに格納
        : rtype : None
        : return : なし
        """
        for i in itertools.combinations("01234", self.list_num_place[0]):
            for j in itertools.combinations("56789", self.list_num_place[1]):
                for k in itertools.combinations("abcde", self.list_num_place[2]):
                    for l in itertools.combinations("f", self.digits-sum(self.list_num_place)):
                        n = "".join(i+j+k+l)
                    self.list_possible_ans_combination.append(n)


    def _first_2_times(self) -> None:
        """進化後, 最初に行う, 答えとなる数字がどのグループに何個あるのか特定
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
            if self.count == 2 or self.room_state == 3:
                break
            else:
                time.sleep(0.5)
                continue

    def _make_list_possible_ans_combination(self) -> None:
        """進化後, 2番目に行う
        最初の2回で作ったlist_ans_numから, 答えの5数字の"組み合わせ"の候補を全て洗い出し,
        list_possible_ans_combinationに格納
        : rtype : None
        : return : なし
        """
        for i in itertools.combinations("01234", self.list_num_place[0]):
            for j in itertools.combinations("56789", self.list_num_place[1]):
                for k in itertools.combinations("abcdef", self.digits-sum(self.list_num_place)):
                    n = "".join(i+j+k)
                    self.list_possible_ans_combination.append(n)


    def _remove_impossible_combination(self) -> None:
        """3番目で使用
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


    def _remove_impossible_permutation(self) -> None:
        """3番目で使用
        そのターンに質問で帰ってきたhitの値を保存し, list_possible_ansの解の候補のjのうち
        self.numとjでhitが一致しないものは答えの"順列"の候補としてありえないので候補から削除
        こうしてlist_possible_ansの中身を削っていく
        : rtype : None
        : return : なし
        """
        hit = self.hit
        for i in self.list_possible_ans[:]:
            self._check_hit_blow(self.num,i)
            # print("hit:{},self_hit:{}, selfnum:{}, k:{}, count:{}".format(hit,self.hit,self.num,i,count))
            if self.hit != hit:
                self.list_possible_ans.remove(i)


    def _check_hit_blow(self,num,ans) -> None:
        """2つのremove関数内で使用
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
        """3番目に行う(1番のメイン部分)
        1秒ごとにget_tableで状態を確認し,
        対戦続行中で,自分のターンのとき, list_ans_num_combinationの中からランダムで質問する数字を選んでself.numに格納
        post_guessし, 帰ってきたhit,blowをprintし, remove_impossible_combinationを行う
        hit+blow = 5の(組み合わせが特定出来た)ときは, まずその結果からあり得る数字の順列120通りのlist_possible_ansを作成
        次にそのターンのhit,blowからあり得ないものを削除し, 順列を考える次の関数(後述)に移る
        自分のターンで無かったら, 0.5秒待機
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
                    if st.session_state.level >= 20:
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
        """3番目で使用
        1秒ごとにget_tableで状態を確認し,
        対戦続行中で,自分のターンのとき, list_ans_numの中からランダムで質問する数字を選んでself.numに格納
        post_guessし, 帰ってきたhitをprintし, remove_impossible_ansを行う
        自分のターンで無かったら, 0.5秒待機
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
            if self.room_state == 3:
                break
            else:
                time.sleep(0.5)
                continue


    def run(self) -> None:
        """ 数当てゲーム実行ランナー
        対戦中の表示を出してから部屋を作成して答えをポストして対戦開始, 終わったら対戦終了と結果の表示
        : rtype : None
        : return : なし
        """
        st.session_state.col2.subheader("{}の現在のレベル : {}".format(st.session_state.chara_name,st.session_state.level))
        st.session_state.col2.write("対戦回数 : {}".format(st.session_state.game_count))
        place = st.session_state.col6.empty()
        self._enterroom_and_registerplayer()
        self._post_hidden_number()
        place.write("対戦中・・・")
        if st.session_state.level >= 20:
            self._first_2_times()
            self._make_list_possible_ans_combination()
        else:
            self._first_3_times()
            self._make_list_possible_ans_combination_3()
        self._identify_number()
        place.write("対戦終了！")
        self._music_stop()
        self._show_result_vscode()
        self._show_result_streamlit()


    def _show_result_vscode(self) -> None:
        """対戦終了後, お互いの結果を表示(vscode上に表示する分)
        : rtype : None
        : return : なし
        """
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

    def _get_information(self) -> str:
        """対戦終了後,web画面に表示する内容を計算
        勝敗,連勝に応じて獲得経験値を求め, 経験値に加える.レベルや次のレベルまでの必要経験値も求める
        レベルアップと進化の判定も行う
        : rtype : str
        : return : 獲得経験値と次のレベルまでの必要経験値
        """
        if self.winner == self.player_name :
            st.session_state.win_in_a_row += 1
            new_exp = round(3000*(1+(st.session_state.win_in_a_row-1)/4)/self.count)
        elif self.winner == None:
            st.session_state.win_in_a_row = 0
            new_exp = round(20*self.count)
        else:
            st.session_state.win_in_a_row = 0
            new_exp = round(15*self.count)

        st.session_state.game_count += 1
        st.session_state.exp += new_exp
        level_up = False
        evolution = False
        for i in range(200):
            if i**3/3 <= st.session_state.exp and st.session_state.exp < (i+1)**3/3:
                remaining_exp = round((i+1)**3/3 - st.session_state.exp)
                new_level = i
                if new_level != st.session_state.level:
                    level_up = True
                    if new_level == 20:
                        evolution = True
                st.session_state.level = new_level
                break
        return new_exp,remaining_exp,level_up,evolution
        # for i in range(200):
        #     if i**3/3 <= st.session_state.exp and st.session_state.exp < (i+1)**3/3:
        #         st.session_state.level = i
        #         remaining_exp = round((i+1)**3/3 - st.session_state.exp)
        #         break
        #     elif i**3/3 >=st.session_state.exp and st.session_state.exp >(i-1)**3/3:
        #         self.remaining_exp_level = round((i)**3/3 - st.session_state.exp)
        # return new_exp,remaining_exp

    def _show_result_streamlit(self) -> None:
        """対戦終了後, お互いの結果を表示(web画面上に表示する分)
        勝敗、連勝数に応じて表示を変える, 経験値やレベル, 対戦回数も表示
        進化やレベルアップの時は追加のエフェクト
        : rtype : None
        : return : なし
        """
        new_exp,remaining_exp,level_up,evolution = self._get_information()
        time.sleep(3)
        st.session_state.col6.subheader("")
        if self.winner == self.player_name:
            self._sound_play(num = 1, title = 'voice/'+st.session_state.chara_name+'/winner.wav')
            self._play_song(num = -1, title = "bgm/winner.wav")
            st.session_state.col6.subheader("勝利だ,おめでとう！")
            st.session_state.col6.subheader("正解は‥【{}】".format(self.num))
            st.session_state.col6.subheader("{}回で正解できた！".format(self.count))
            st.session_state.col6.subheader("")
            if st.session_state.win_in_a_row >= 2:
                st.session_state.col6.subheader("すごいぞ,{}連勝だ！この調子！".format(st.session_state.win_in_a_row))
            st.balloons()
        elif self.winner == None:
            self._sound_play(num = 1, title = 'voice/'+st.session_state.chara_name+'/draw.wav')
            self._play_song(num = -1, title = 'bgm/draw.mp3')
            st.session_state.col6.subheader("引き分けだ！ ")
            st.session_state.col6.subheader("正解は‥【{}】".format(self.num))
            st.session_state.col6.subheader("{}回で正解した！".format(self.count))
        else:
            self._sound_play(num = 1, title = 'voice/'+st.session_state.chara_name+'/loser.wav')
            self._play_song(num = -1, title = "bgm/loser.wav")
            st.session_state.col6.subheader("負けてしまった・・・次は勝とう！")

        st.session_state.col6.write("{}は{}経験値を得た！".format(st.session_state.chara_name,new_exp))
        st.session_state.col6.write("履歴")
        st.session_state.col6.write("")
        st.session_state.col6.write(self.my_history)
        time.sleep(13)

        if level_up:
            self._music_stop()
            if evolution:
                st.session_state.col4.subheader("おや?{}の様子が...".format(st.session_state.chara_name))
                image_light = Image.open('picture/evolution_light.png')
                st.session_state.col4.image(image_light)
                self._play_song(num = 1,title = "bgm/evolution_light.mp3")
                time.sleep(3)

                st.session_state.col6.subheader("やったね, 進化した！")
                pic_url2 = "picture/"+st.session_state.chara_name+"-2.jpg"
                image = Image.open(pic_url2)
                st.session_state.col4.image(image)
                img = Image.open('picture/evolution.gif')
                st.session_state.col6.image(img)
                self._play_song(num = 1,title = "bgm/evolution.mp3")
                time.sleep(3)
            else:
                st.session_state.col6.subheader("レベルアップだ！")
                self._play_song(num = 1,title = "bgm/level_up.wav")
                img = Image.open('picture/level-up.gif')
                time.sleep(1)
                st.session_state.col6.image(img)

        time.sleep(1)
        st.session_state.col6.write("次のレベルまでの経験値：{}".format(remaining_exp))
        st.session_state.col6.write("今まで得た合計経験値：{}".format(st.session_state.exp))
        st.session_state.col6.subheader("")
        st.session_state.col6.subheader("{}の現在のレベル : {}".format(st.session_state.chara_name,st.session_state.level))
        st.session_state.col6.write("対戦回数 : {}".format(st.session_state.game_count))
