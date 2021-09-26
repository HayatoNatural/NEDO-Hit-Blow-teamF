import random
from typing import List,Tuple
import itertools
import argparse

class Numberguess:
    
    def __init__(self,max_count=250,ans=None) -> None:
        self.max_count = max_count
        self.digits = 5
        self.count = 0
        self.history = []
        self.list_where_num_is = []
        self.List_ans_num = []
        self.List_16 = ["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"]
        if ans is not None:
            self.ans = ans
        else:
            self.ans = self._define_answer()
        self.num = None
        self.hit = None
        self.blow = None
        self.list_possible_ans = []

    def _define_answer(self) -> str:
        ans_list = random.sample(self.List_16, self.digits)
        ans = "".join(ans_list)
        return ans

    def _get_your_num(self) -> str :
        while True:
            num = input("16進数で5桁の重複しない数字を入力してください ==> ")
            judge = True
            for i in num:
                if i not in self.List_16:
                    judge = False
            if judge == True and len(num) == self.digits and len(set(num)) == self.digits:
                return num
            else:
                print("もう一度入力しなおしてください(16進数, 5桁, 重複なし)")


    def _play_game_manual(self) -> None:
        for self.count in range(self.max_count):
            print("{}回目, 残りの入力回数は{}回です".format(self.count+1, self.max_count-self.count))
            self.num = self._get_your_num()
            self.history.append(self.num)
            self.count += 1 
            self._show_hit_blow()
            print("!!  {} Hit, {} Blow  !!".format(self.hit,self.blow))
            if self.hit == self.digits:
                print("!! 正解です !!")
                break

    def _show_hit_blow(self) -> None:
        self.hit = 0
        self.blow = 0
        for i in range(self.digits):
            if self.num[i] == self.ans[i]:
                self.hit += 1
            else:
                if self.num[i] in self.ans:
                    self.blow += 1

    def _make_list_possible_ans(self):
        for i in itertools.permutations(self.List_16,5):
            n = "".join(i)
            self.list_possible_ans.append(n)

    def _remove_impossible_ans(self):
        for k in self.list_possible_ans:
            self.num = k
            hit = self.hit
            blow = self.blow
            self._show_hit_blow()
            if self.hit != hit or self.blow != blow:
                self.list_possible_ans.remove(k)

    def _first_three_times(self) -> None:
        search_list = ["01234","56789","abcde"]
        for i in range(3):
            print("{}回目, 残りの入力回数は{}回です".format(self.count+1, self.max_count-self.count))
            self.num = search_list[i]
            self.history.append(self.num)
            self.count += 1
            self._show_hit_blow()
            self.list_where_num_is.append(self.hit + self.blow)
            print("-----",self.num)
            print("!!  {} Hit, {} Blow  !!".format(self.hit,self.blow))
            if self.hit == self.digits:
                print("!! 正解です !!")
                break
        else:
            print("----------from first3 to 5C----------")


    def _identify_5_numbers(self) -> None:
        for i in itertools.combinations("01234", self.list_where_num_is[0]):
            for j in itertools.combinations("56789", self.list_where_num_is[1]):
                for k in itertools.combinations("abcde", self.list_where_num_is[2]):
                    for l in itertools.combinations("f", self.digits-sum(self.list_where_num_is)):                
                        print("{}回目, 残りの入力回数は{}回です".format(self.count+1, self.max_count-self.count))
                        self.num = "".join(i+j+k+l)
                        self.history.append(self.num)
                        self.count += 1
                        self._show_hit_blow()
                        print("-----",self.num)
                        print("!!  {} Hit, {} Blow  !!".format(self.hit,self.blow))
                        if self.hit == self.digits:
                            print("!! 正解です !!")
                            break
                        elif self.hit + self.blow == self.digits:
                            self.List_ans_num = [i for i in self.num]
                            print("----------------from 5C to 5P-------------------")
                            self._identify_permutation()
                            break
                        elif not 0 in self.list_where_num_is and self.hit+self.blow == self.digits-1:
                            print("---------------from 5C to 4--------------------")
                            self._sum_hitblow_4()
                            print("---------------from 4 to 5P--------------------")
                            self._identify_permutation()
                            break
                    else:
                        continue
                    break           
                else:
                    continue
                break           
            else:
                continue
            break           


    def _sum_hitblow_4(self):
        num_set = set(self.num)
        for i in itertools.combinations(sorted(num_set), 4):
            for j in itertools.combinations(sorted(set(self.List_16) ^ num_set),1):
                print("{}回目, 残りの入力回数は{}回です".format(self.count+1, self.max_count-self.count))
                self.num = "".join(i+j)
                self.history.append(self.num)
                self.count += 1 
                self._show_hit_blow()
                print("-----",self.num)
                print("!!  {} Hit, {} Blow  !!".format(self.hit,self.blow))
                if self.hit == self.digits:
                    print("!! 正解です !!")
                    break
                elif self.hit + self.blow == self.digits:
                    self.List_ans_num = [i for i in self.num]
                    break
            else:
                continue
            break           


    def _identify_permutation(self) -> None:
        for i in itertools.permutations(sorted(self.List_ans_num), self.digits):
            print("{}回目, 残りの入力回数は{}回です".format(self.count+1, self.max_count-self.count))
            self.num = "".join(i)
            self.history.append(self.num)
            self.count += 1
            self._show_hit_blow()
            print("-----",self.num)
            print("!!  {} Hit, {} Blow  !!".format(self.hit,self.blow))
            if self.hit == self.digits:
                print("!! 正解です !!")
                break

    
    def _play_game_auto(self) -> None:
        self._first_three_times()
        self._identify_5_numbers()



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
        self._show_result()


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

def get_parser() -> argparse.Namespace:
    """コマンドライン引数を解析したものを持つ
    :rtype : argparse.Namespace
    :return : コマンド値
    """
    parser = argparse.ArgumentParser(description="Hit&Blow, 数当てゲーム")
    parser.add_argument("--ans")
    parser.add_argument("--mode",default="auto")

    args = parser.parse_args()
    return args

def main() -> None:
    """Hit&Blowのメイン
    """
    args = get_parser()
    mode = args.mode
    ans= args.ans

    if args.ans is not None:
        runner = Numberguess(ans=ans)
    else:
        runner = Numberguess()

    runner.run(mode=mode)

if __name__ == "__main__":
    main()

