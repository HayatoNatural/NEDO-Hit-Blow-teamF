import random
from typing import List,Tuple
import itertools
import argparse

class Numberguess2:
    
    def __init__(self,ans=None) -> None:
        self.digits = 5
        self.count = 0
        self.history = []
        self.List_16 = ["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"]
        self.list_num_place = []
        self.list_possible_ans = []
        self.list_ans_combination = []
        if ans is not None:
            self.ans = ans
        else:
            self.ans = self._define_answer()
        self.num = None

    def _define_answer(self) -> str:
        ans_list = random.sample(self.List_16, self.digits)
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


    def _first_three_times(self) -> None:
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

    def _make_list_possible_ans(self) -> None:
        for i in itertools.combinations("01234", self.list_num_place[0]):
            for j in itertools.combinations("56789", self.list_num_place[1]):
                for k in itertools.combinations("abcde", self.list_num_place[2]):
                    for l in itertools.combinations("f", self.digits-sum(self.list_num_place)):
                        n = "".join(i+j+k+l)
                        self.list_possible_ans.append(n)

    def _remove_impossible_combination(self):
        hb = self.hit + self.blow
        for j in self.list_possible_ans:
            self._check_hit_blow(self.num,j)
            if self.hit +self.blow != hb :
                self.list_possible_ans.remove(j)

    def _remove_impossible_permutation(self):
        hit = self.hit
        blow = self.blow
        for k in self.list_possible_ans:
            self._check_hit_blow(self.num,k)
            if self.hit != hit or self.blow != blow:
                self.list_possible_ans.remove(k)


    def _identify_number(self):
        print("----------from first3 to 5C----------")
        while True:
            print("{}回目の入力です".format(self.count+1))
            self.num = random.choice(self.list_possible_ans)
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
                self.list_possible_ans = []
                for i in itertools.permutations(self.list_ans_combination,5):
                    m = "".join(i)
                    self.list_possible_ans.append(m)
                print("----------from 5C to 5P----------")
                self._identify_permutation()
                break
            else:
                self._remove_impossible_combination()

    def _identify_permutation(self):
        while True:
            print("{}回目の入力です".format(self.count+1))
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


    def _show_result(self) -> None:
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

    def _play_game_auto(self) -> None:
        self._first_three_times()
        self._make_list_possible_ans()
        self._identify_number()
        self._show_result()


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

    runner._play_game_auto()

if __name__ == "__main__":
    main()

