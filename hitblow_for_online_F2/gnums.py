import random

class hit_and_blow():
    def __init__(self) -> None:
        self.numbers=self.createNum()
        self.guesstimes=0
        self.npc=0
        self.nc=0


    def createNum(self) ->int: # Generate the right answer.
        n=4
        no=[]
        while n>0:
            number=str(random.randint(0,9))
            while number in no: # Reject repeated number.
                number = str(random.randint(0,9))
            no.append(number)
            n-=1
        return no


    def guess_numbers(self) ->int:
        while True:
            input_str=input("Please input your numbers:")
            if len(input_str)==4 and input_str.isdecimal():
                gnums=list(input_str)
                if len(set(gnums))==4:
                    return gnums
                else:
                    print("Numbers should be different.")
            else:
                print("Input is wrong. Please try again.")


    def play_game_manual(self):
        while self.npc<4:
            gnums=self.guess_numbers()
            i=0
            for m in gnums:
                if m in self.numbers:
                    self.nc+=1
                    if self.numbers[i]==gnums[i]:
                        self.npc+=1
                        self.nc-=1
                i+=1
            print("{}A{}B".format(self.npc,self.nc))
            self.guesstimes+=1


    def run(self, mode="manual"):
        if mode=="manual":
            self.play_game_manual()
        else:
            self.play_game_auto()
        self.show_result()


    def show_result(self):
        times=self.guesstimes
        if times<8:
            print("Excellent. You only tried {} times to get the right answer.".format(times))
        else:
            print("You are finally right. {} times were too many.".format(times))


def main():
    print("Game is on.")
    runner=hit_and_blow()
    runner.run("manual")


if __name__== "__main__":
    main()    
