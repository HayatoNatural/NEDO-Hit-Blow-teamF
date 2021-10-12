# coding : UTF-8
"""
File Name: hitblow_solo_manual.py
Description: Hit&Blowの手動一人対戦モード
Created on october 13,2021
Created by Hayato Mori, Kaito Isshiki, Chao Wang
"""
import random
import argparse
import time
from PIL import Image
import streamlit as st
import pygame
st.set_page_config(layout="wide")
col1,col2 =st.columns([4,1])
col4,space,col6 =st.columns([7,1,4])

def initialize_streamlit() -> None:
    """クラスを定義する前にweb上で画面を出しておく
    状態量として, 試合数, 経験値, レベル, 連勝数を定義し, 初期化しておく(マジックコマンド的な)
    : rtype : None
    : return : なし
    """
    col1.title("Welcome to Hit&Blow Game！16進数5桁の秘密の数字を当てよう！")
    col1.subheader("対戦すると経験値がもらえるよ. 経験値は当てた回数や連勝数に応じて増えるぞ！")
    col1.subheader("経験値が貯まるとレベルアップだ！いずれはキャラが進化するかも‥？")
    if 'game_count' not in st.session_state:
        st.session_state.game_count = 1
    if 'exp' not in st.session_state:
        st.session_state.exp = 0
    if 'level' not in st.session_state:
        st.session_state.level = 1
    if 'win_in_a_row' not in st.session_state:
        st.session_state.win_in_a_row = 1
    if 'turn_count' not in st.session_state:
        st.session_state.turn_count= 0
    if 'history' not in st.session_state:
        st.session_state.history= {}
    name = col4.selectbox("キャラクターを選んでね",["ジャック","クリス","フローラ","ドロシー"])
    st.session_state.chara_name = name
    pic_url1 = "picture/"+name+"-1.jpg"
    pic_url2 = "picture/"+name+"-2.jpg"
    if st.session_state.level < 20:
        image = Image.open(pic_url1)
        col4.image(image)
    else:
        image = Image.open(pic_url2)
        col4.image(image)
    col6.subheader("{}の現在のレベル : {}".format(st.session_state.chara_name,st.session_state.level))
    col6.write("対戦回数 : {}".format(st.session_state.game_count-1))


class Playgame_solo_manual:
    """16進数5桁のHit&Blow　自動一人対戦の数当てモード

    :param int digits : 数の桁数
    :param set Tuple_16 : 数に使う16進数の数字の集合
    :param str ans : comの答え(自分が当てる数字)
    :param List[dict] my_history : 自分が相手の数当をした時の履歴
    :param str num : こちらが予想した相手の数字
    :param int hit : 数字のhit数
    :param int blow : 数字のblow数
    :param int volume:音量(0～1で変更)
    """


    def __init__(self,ans=None,num=None) -> None:
        self.digits = 5
        self.Tuple_16 = ("0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f")
        self.hit = None
        self.blow = None
        self.volume = 0.3
        if ans is not None:
            self.ans = ans
        else:
            self.ans = self._define_answer()
        if 'ans' not in st.session_state:
            st.session_state.ans= self.ans
        self.num = num

    def _define_answer(self) -> str:
        """自分が当てる答えをつくる
        : rtype : str
        : return : ans
        """
        ans_list = random.sample(self.Tuple_16, self.digits)
        ans = "".join(ans_list)
        return ans


    def _play_song(self,num:int, title):
        """待機時間中音楽再生
        :param int num:再生回数(-1で無限ループ，これを使って止めたいときにstopするのが良いかと)
        :param int playtime:再生時間(基本-1で無限ループしてるので、使わない．デフォルト値Noneで良い)
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


    def _check_hit_blow(self,num,ans) -> None:
        """メインで使用
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

    def _play_game_manual(self) -> None:
        """ 手動一人対戦の数当てゲーム
        対戦中の表示を出してから部屋を作成して答えをポストして対戦開始, 終わったら対戦終了と結果の表示
        : rtype : None
        : return : なし
        """
        self._music_stop()
        place = col6.empty()
        place.write("対戦中・・・")
        self._play_song(num = 1,title = "bgm/game_start.wav")
        time.sleep(3)
        self._play_song(num = -1,title = "bgm/Battle.wav")
        print("aaaaa")
        self._check_hit_blow(self.num,st.session_state.ans)
        st.session_state.history[self.num] = [str(self.hit)+"hit", str(self.blow)+"blow"]
        st.session_state.turn_count += 1
        print("!!  {} Hit, {} Blow  !!".format(self.hit,self.blow))
        col6.subheader("{} Hit, {} Blowだ！".format(self.hit,self.blow))
        col6.write("現在のターン数,{}".format(st.session_state.turn_count))
        col6.write("今までの入力履歴,{}".format(st.session_state.history))
        if self.hit == self.digits:
            print("!! 正解です !!")
            place.write("対戦終了！")
            self._show_result_vscode()
            self._show_result_streamlit()


    def _show_result_vscode(self) -> None:
        """対戦終了後, お互いの結果を表示(vscode上に表示する分)
        : rtype : None
        : return : なし
        """
        print("------------------------")
        print("show history")
        print(st.session_state.history)
        print("------------------------")
        print("正解は{}です. おめでとうございます！ {}回で正解しました.".format(st.session_state.ans,st.session_state.turn_count))
        print("------------------------")


    def _get_information(self) -> str:
        """対戦終了後,web画面に表示する内容を計算
        勝敗,連勝に応じて獲得経験値を求め, 経験値に加える.レベルや次のレベルまでの必要経験値も求める
        進化やレベルアップの判定も行う
        : rtype : str
        : return : 獲得経験値と次のレベルまでの必要経験値
        """
        # st.session_state.win_in_a_row += 1
        level_up = False
        evolution = False
        new_exp = round(3000*(1+(st.session_state.win_in_a_row-1)/4)/st.session_state.turn_count)
        st.session_state.exp += new_exp
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

    def _show_result_streamlit(self) -> None:
        """対戦終了後, お互いの結果を表示(web画面上に表示する分)
        勝敗、連勝数に応じて表示を変える, 経験値やレベル, 対戦回数も表示
        進化とレベルアップの時は追加エフェクト
        : rtype : None
        : return : なし
        """
        new_exp,remaining_exp,level_up,evolution = self._get_information()
        self._music_stop()
        self._play_song(num = -1, title = "bgm/winner.wav")
        col6.subheader("")
        col6.subheader("勝利だ,おめでとう！")
        col6.subheader("正解は‥【{}】{}回で正解できた！".format(self.num,st.session_state.turn_count))
        col6.subheader("")
        # if st.session_state.win_in_a_row >= 2:
        #     col6.subheader("すごいぞ,{}連勝だ！その調子！".format(st.session_state.win_in_a_row))
        time.sleep(3)
        st.balloons()
        col6.write("{}は{}経験値を得た！".format(st.session_state.chara_name,new_exp))
        col6.write("")
        time.sleep(13)
        if level_up:
            if evolution:
                col4.subheader("おや?{}の様子が...".format(st.session_state.chara_name))
                image_light = Image.open('picture/evolution_light.png')
                col4.image(image_light)
                self._play_song(num = 1,title = "bgm/evolution_light.mp3")
                time.sleep(3)
                col4.subheader("やったね, 進化した！")
                pic_url2 = "picture/"+st.session_state.chara_name+"-2.jpg"
                image = Image.open(pic_url2)
                col4.image(image)
                img = Image.open('picture/evolution.gif')
                col6.image(img)
                self._play_song(num = 1,title = "bgm/evolution.mp3")
                time.sleep(3)
            else:
                col6.subheader("レベルアップだ！")
                self._music_stop()
                self._play_song(num = 1,title = "bgm/level_up.wav")
                img = Image.open('picture/level-up.gif')
                time.sleep(1)
                col6.image(img)
        col6.write("次のレベルまでの経験値：{}".format(remaining_exp))
        col6.write("今まで得た合計経験値：{}".format(st.session_state.exp))
        col6.subheader("")
        col6.subheader("{}の現在のレベル : {}".format(st.session_state.chara_name,st.session_state.level))
        col6.write("対戦回数 : {}".format(st.session_state.game_count))
        col6.subheader("また新たな秘密の数字が現れた！当てに行こう！")
        st.session_state.game_count += 1
        st.session_state.turn_count = 0
        st.session_state.history = {}
        st.session_state.ans = self._define_answer()


def get_parser() -> argparse.Namespace:
    """コマンドライン引数を解析したものを持つ
    :rtype : argparse.Namespace
    :return : コマンド値
    """
    parser = argparse.ArgumentParser(description="Hit&Blow, 数当てゲーム")
    parser.add_argument("--ans",default=None)
    args = parser.parse_args()
    return args

def main() -> None:
    """Hit&Blowのメイン
    """
    args = get_parser()
    ans= args.ans

    initialize_streamlit()
    num = col6.text_input("予想する数字を入力してね")

    if args.ans is not None:
        runner = Playgame_solo_manual(ans=ans,num=num)
    else:
        runner = Playgame_solo_manual(num=num)
    runner._play_song(num = -1,title = 'bgm/waiting.wav')

    if col6.button("クリックすると数字をチェックするよ!"):
        runner._play_game_manual()

if __name__ == "__main__":
    main()
