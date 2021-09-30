# coding : UTF-8
"""
File Name: hitblow.py
Description: Hit&Blowの実行
Created on September 25,2021
Created by Hayato Mori, Kaito Isshiki, Chao Wang
"""
import argparse
from class_play_game import Playgame

def get_parser() -> argparse.Namespace:
    """コマンドライン引数を解析したものを持つ
    :rtype : argparse.Namespace
    :return : コマンド値
    """
    parser = argparse.ArgumentParser(description="Hit&Blow, 数当てゲーム")
    parser.add_argument("--ans",default=None)
    parser.add_argument("--mode",default="auto")
    parser.add_argument("--roomid",default="6016")

    args = parser.parse_args()
    return args

def main() -> None:
    """Hit&Blowのメイン
    """
    args = get_parser()
    mode = args.mode
    room_id = args.roomid
    ans= args.ans

    if args.ans is not None:
        runner = Playgame(ans=ans,room_id=room_id)
    else:
        runner = Playgame(room_id=room_id)

    runner.run(mode=mode)

if __name__ == "__main__":
    main()
