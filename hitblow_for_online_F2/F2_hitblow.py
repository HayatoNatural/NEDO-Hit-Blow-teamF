# coding : UTF-8
"""
File Name: hitblow.py
Description: Hit&Blowの実行
Created on october 7,2021
Created by Hayato Mori, Kaito Isshiki, Chao Wang
"""
import argparse
import time
import streamlit as st
from F2_class_play_game import Playgame,initialize_streamlit

def get_parser() -> argparse.Namespace:
    """コマンドライン引数を解析したものを持つ
    :rtype : argparse.Namespace
    :return : コマンド値
    """
    parser = argparse.ArgumentParser(description="Hit&Blow, 数当てゲーム")
    parser.add_argument("--ans",default=None)
    parser.add_argument("--mode",default="auto")
    # parser.add_argument("--roomid",default="6056")

    args = parser.parse_args()
    return args

def main() -> None:
    """Hit&Blowのメイン,パーサーは無くていいかも
    web画面だけ表示しておいて, ボタンを押すと部屋作成ー自動対戦が始まる
    """
    initialize_streamlit()
    room_id = st.number_input('部屋番号を入力してね',min_value=6100)

    args = get_parser()
    mode = args.mode
    # room_id = args.roomid
    ans= args.ans
    if args.ans is not None:
        runner = Playgame(ans=ans,room_id=room_id)
    else:
        runner = Playgame(room_id=room_id)

    if st.button("クリックすると部屋を作成して対戦を始めるよ"):
        time.sleep(3)
        runner.run(mode=mode)

if __name__ == "__main__":
    main()
