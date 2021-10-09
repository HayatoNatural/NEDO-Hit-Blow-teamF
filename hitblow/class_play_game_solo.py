import random
import itertools
import argparse
import streamlit as st
from PIL import Image

class Playgame_solo:

    def __init__(self,ans=None) -> None:
        self.digits = 5
        self.count = 0
        self.Tuple_16 = ("0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f")
        self.hit = None
        self.blow = None
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
        self.picture_place = st.empty()

    def _define_answer(self) -> str:
        ans_list = random.sample(self.Tuple_16, self.digits)
        ans = "".join(ans_list)
        return ans

    def initialize_streamlit(self) ->None:
        """クラスを定義する前にweb上で画面を出しておく
        状態量として, 試合数, 経験値, レベル, 連勝数を定義し, 初期化しておく(マジックコマンド的な)
        : rtype : None
        : return : なし
        """
        st.title("Welcome to Hit&Blow World!")
        st.subheader("1:1の数当てゲームで対戦だ！")
        st.markdown("**_524160_**通りから相手の数字を当ててレベルアップしよう！")
        if 'game_count' not in st.session_state:
            st.session_state.game_count = 0
        if 'exp' not in st.session_state:
            st.session_state.exp = 0
        if 'level' not in st.session_state:
            st.session_state.level = 1
        if 'win_in_a_row' not in st.session_state:
            st.session_state.win_in_a_row = 0
        if st.session_state.level <=20:
            image = Image.open('picture.jpg')
            st.image(image)
        else:
            image = Image.open('picture_scene.jpg')
            st.image(image)


    def _get_your_num(self) -> str :
        while True:
            num = input("16進数で5桁の重複しない数字を入力してね --> ")
            judge = True
            for i in num:
                if i not in self.Tuple_16:
                    judge = False
            if judge == True and len(num) == self.digits and len(set(num)) == self.digits:
                return num
            else:
                print("もう一度入力しなおしてください(16進数, 5桁, 重複なし)")


    def _play_game_manual(self) -> None:
        while True:
            print("{}回目, 残りの入力回数は{}回です".format(self.count+1, 30-self.count))
            self.num = self._get_your_num()
            self.history.append(self.num)
            self.count += 1
            self._check_hit_blow(self.num,self.ans)
            print("!!  {} Hit, {} Blow  !!".format(self.hit,self.blow))

            if self.hit == self.digits:
                print("!! 正解です !!")
                break


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

    def _make_list_possible_ans_combination_3(self) -> None:
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

    def _make_list_possible_ans_combination(self) -> None:
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
            self.num = random.choice(self.list_possible_ans_combination)
            self.history.append(self.num)
            self.count += 1
            self._check_hit_blow(self.num,self.ans)
            print("-----",self.num)
            print("!!  {} Hit, {} Blow  !!".format(self.hit,self.blow))
            if self.hit == self.digits:
                print("!! 正解です !!")
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
            print("{}回目の入力です, 順列の候補は{}通りです.".format(self.count+1,len(self.list_possible_ans)))
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

    def _get_experience(self) -> str:
        """対戦終了後,web画面に表示する内容を計算
        勝敗,連勝に応じて獲得経験値を求め, 経験値に加える.レベルや次のレベルまでの必要経験値も求める
        : rtype : str
        : return : 獲得経験値と次のレベルまでの必要経験値
        """
        st.session_state.win_in_a_row += 1
        level_up = False
        evolution = False
        new_exp = round(3000*(1+(st.session_state.win_in_a_row-1)/4)/self.count)
        st.session_state.game_count += 1
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
        : rtype : None
        : return : なし
        """
        new_exp,remaining_exp,level_up,evolution = self._get_experience()
        st.subheader("勝利だ,おめでとう！正解は‥【{}】！".format(self.num))
        st.subheader("{}回で正解できた！".format(self.count))
        left,right = st.columns(2)
        if st.session_state.win_in_a_row >= 2:
            left.write("すごいぞ,{}連勝だ！この調子！".format(st.session_state.win_in_a_row))
            # time.sleep(1)
        st.balloons()
        left.write("君は{}経験値を得た！".format(new_exp,st))
        left.write("対戦回数 : {}".format(st.session_state.game_count))
        if level_up:
            right.write('<span style="color:red;background:black">レベルアップだ！</span>',unsafe_allow_html=True)
        if evolution:
            right.write('<span style="color:green;background:black">やったね,進化した！</span>',unsafe_allow_html=True)
        right.write("君の現在のレベル : {}".format(st.session_state.level))
        right.write("次のレベルまでの経験値：{}".format(remaining_exp))
        right.write("今まで得た合計経験値：{}".format(st.session_state.exp))

    def _play_game_auto(self) -> None:
        self._first_2_times()
        self._make_list_possible_ans_combination()
        self._identify_number()

    def run(self, mode="auto") -> None:
        """ 数当てゲーム実行ランナー
        : param str mode : ゲームの実行モード("manual","linear","binary")
        : rtype : None
        : return : なし
        """
        if mode == "auto":
            self._play_game_auto()
        else:
            self._play_game_manual()

        self._show_result_vscode()
        self._show_result_streamlit()


def get_parser() -> argparse.Namespace:
    """コマンドライン引数を解析したものを持つ
    :rtype : argparse.Namespace
    :return : コマンド値
    """
    parser = argparse.ArgumentParser(description="Hit&Blow, 数当てゲーム")
    parser.add_argument("--ans",default=None)
    parser.add_argument("--mode",default="auto")
    args = parser.parse_args()
    return args

def main() -> None:
    """Hit&Blowのメイン
    """
    args = get_parser()
    ans= args.ans
    mode = args.mode

    if args.ans is not None:
        runner = Playgame_solo(ans=ans)
    else:
        runner = Playgame_solo()

    runner.initialize_streamlit()
    if st.button("クリックすると対戦が始まるよ!"):
        # time.sleep(1)
        runner.run(mode=mode)

if __name__ == "__main__":
    main()
