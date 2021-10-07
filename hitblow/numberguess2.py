from logging import PlaceHolder
import random
from typing import List,Tuple
import itertools
import argparse
import streamlit as st
import time
import math
from PIL import Image

class Numberguess2:

    def __init__(self,ans=None) -> None:
        self.digits = 5
        self.count = 0
        self.history = []
        self.list_num_place = []
        self.list_possible_ans_combination = []
        self.list_ans_combination = []
        self.list_possible_ans = []
        if ans is not None:
            self.ans = ans
        else:
            self.ans = self._define_answer()
        self.num = None
        self.player_level = 1
        self.win_in_a_row = 1


    def _define_answer(self) -> str:
        Tuple_16 = ("0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f")
        ans_list = random.sample(Tuple_16, self.digits)
        ans = "".join(ans_list)
        return ans


    def _check_hit_blow(self,num,ans) -> None:
        self.hit = 0
        self.blow = 0
        for i in range(self.digits):
            if num[i] == ans[i]:
                self.hit += 1
            else:
                if num[i] in ans:
                    self.blow += 1


    def _first_3_times(self) -> None:
        search_list = ["01234","56789","abcde"]
        for i in range(3):
            print("{}回目の入力です".format(self.count+1))
            self.num = search_list[i]
            self.history.append(self.num)
            self.count += 1
            self._check_hit_blow(self.num,self.ans)
            self.list_num_place.append(self.hit+self.blow)
            print("-----",self.num)
            print("!!  {} Hit, {} Blow  !!".format(self.hit,self.blow))
            if self.hit == self.digits:
                print("!! 正解です !!")
                break

    def _make_list_possible_ans_combination(self) -> None:
        for i in itertools.combinations("01234", self.list_num_place[0]):
            for j in itertools.combinations("56789", self.list_num_place[1]):
                for k in itertools.combinations("abcde", self.list_num_place[2]):
                    for l in itertools.combinations("f", self.digits-sum(self.list_num_place)):
                        n = "".join(i+j+k+l)
                        self.list_possible_ans_combination.append(n)


    def _first_2_times(self) -> None:
        search_list = ["01234","56789"]
        for i in range(2):
            print("{}回目の入力です".format(self.count+1))
            self.num = search_list[i]
            self.history.append(self.num)
            self.count += 1
            self._check_hit_blow(self.num,self.ans)
            self.list_num_place.append(self.hit+self.blow)
            print("-----",self.num)
            print("!!  {} Hit, {} Blow  !!".format(self.hit,self.blow))
            if self.hit == self.digits:
                print("!! 正解です !!")
                break

    def _make_list_possible_ans_combination_2(self) -> None:
        for i in itertools.combinations("01234", self.list_num_place[0]):
            for j in itertools.combinations("56789", self.list_num_place[1]):
                    for k in itertools.combinations("abcdef", self.digits-sum(self.list_num_place)):
                        n = "".join(i+j+k)
                        self.list_possible_ans_combination.append(n)


    def _remove_impossible_combination(self):
        hb = self.hit + self.blow
        for i in self.list_possible_ans_combination[:]:
            self._check_hit_blow(self.num,i)
            if self.hit + self.blow != hb:
                self.list_possible_ans_combination.remove(i)

    def _remove_impossible_permutation(self):
        hit = self.hit
        for i in self.list_possible_ans[:]:
            self._check_hit_blow(self.num,i)
            # print("hit:{},self_hit:{}, selfnum:{}, k:{}, count:{}".format(hit,self.hit,self.num,i,count))
            if self.hit != hit:
                self.list_possible_ans.remove(i)


    def _identify_number(self):
        print("----------from first3 to 5C----------")
        while True:
            print("{}回目の入力です, 組み合わせの候補は{}通りです.".format(self.count+1,len(self.list_possible_ans_combination)))
            # print(self.list_possible_ans_combination)
            self.num = random.choice(self.list_possible_ans_combination)
            self.history.append(self.num)
            self.count += 1
            self._check_hit_blow(self.num,self.ans)
            print("-----",self.num)
            print("!!  {} Hit, {} Blow  !!".format(self.hit,self.blow))
            if self.hit == self.digits:
                print("正解です！")
                break
            elif self.hit + self.blow == self.digits:
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

    def _identify_permutation(self):
        while True:
            print("--------------------")
            print("{}回目の入力です, 順列の候補は{}通りです.".format(self.count+1,len(self.list_possible_ans)))
            print(self.list_possible_ans)
            self.num = random.choice(self.list_possible_ans)
            self.history.append(self.num)
            self.count += 1
            self._check_hit_blow(self.num,self.ans)
            print("-----",self.num)
            print("!!  {} Hit, {} Blow  !!".format(self.hit,self.blow))
            if self.hit == self.digits:
                print("正解です！")
                break
            self._remove_impossible_permutation()


    def _show_result_vscode(self) -> None:
        print("------------------------")
        print("show history")
        for k,v in enumerate(self.history):
            print("{}回目 : {} ".format(k+1,v))

        print("------------------------")
        if self.history[-1] == self.ans:
            print("正解は{}です. おめでとうございます！ {}回で正解しました.".format(self.ans,self.count))
        else:
            print("正解は{}でした".format(self.ans))

        print("------------------------")

    def _show_result_streamlit(self):
        st.subheader("正解は‥【{}】！ やったね, {}回で正解できた！".format(self.ans,self.count))
        new_exp,remaining_exp = self._get_experience()
        st.write("君は{}経験値を得た！今まで得た合計経験値は{}だ！".format(new_exp,st.session_state.exp))
        st.write("君の現在のレベル : {}, 次のレベルまであと{}経験値だ！".format(st.session_state.level,remaining_exp))
        st.write("対戦回数 : {}".format(st.session_state.game_count))
        time.sleep(1)
        st.balloons()

    def _get_experience(self):
        new_exp = round(3000*(1+(self.win_in_a_row-1)/4)/self.count)
        st.session_state.game_count += 1
        st.session_state.exp += new_exp
        for i in range(200):
            if i**3/3 <= st.session_state.exp and st.session_state.exp < (i+1)**3/3:
                st.session_state.level = i
                remaining_exp = round((i+1)**3/3 - st.session_state.exp)
                break
        return new_exp,remaining_exp

    def _play_game_auto(self) -> None:
        self._first_3_times()
        self._make_list_possible_ans_combination()
        self._identify_number()
        self._show_result_vscode()
        self._show_result_streamlit()

    def _initialize_streamlit(self):
        st.title("Welcome to Hit&Blow World!")
        st.subheader("ここは, 1:1の数当てゲームで勝負する世界.")
        st.subheader("524160通りから, 相手の数字を当てて強くなろう！")
        st.image("picture.jpg")
        if 'game_count' not in st.session_state:
            st.session_state.game_count = 0
        if 'exp' not in st.session_state:
            st.session_state.exp = 0
        if 'level' not in st.session_state:
            st.session_state.level = 1


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
    if args.ans is not None:
        runner = Numberguess2(ans=ans)
    else:
        runner = Numberguess2()

    runner._initialize_streamlit()
    if st.button("クリックすると対戦が始まるよ!"):
        runner._play_game_auto()

if __name__ == "__main__":
    main()
