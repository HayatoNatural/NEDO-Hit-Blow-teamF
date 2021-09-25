import argparse
from setup_and_play_game import Playgame

def get_parser() -> argparse.Namespace:
    """コマンドライン引数を解析したものを持つ

    """
    parser = argparse.ArgumentParser(description="Hit&Blow, 数当てゲーム")
    parser.add_argument("--ans",default="01245")
    parser.add_argument("--mode",default="manual")
    parser.add_argument("--room_id",default="6009")

    args = parser.parse_args()
    return args

def main() -> None:
    """数当てゲームのメイン
    """
    args = get_parser()
    mode = args.mode
    room_id = args.room_id
    ans= args.ans

    if args.ans is not None:
        runner = Playgame(ans=ans,room_id=room_id)
    else:
        runner = Playgame(room_id=room_id)

    runner.run(mode=mode)

if __name__ == "__main__":
    main()
