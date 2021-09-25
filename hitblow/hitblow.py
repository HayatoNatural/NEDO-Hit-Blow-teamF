import argparse
from setup_and_play_game import Setupgame, Playgame

def get_parser() -> argparse.Namespace:
    """コマンドライン引数を解析したものを持つ

    """
    parser = argparse.ArgumentParser(description="Hit&Blow, 数当てゲーム")
    parser.add_argument("--ans")
    parser.add_argument("--mode",default="manual")
    args = parser.parse_args()
    return args

def main() -> None:
    """数当てゲームのメイン
    """
    args = get_parser()
    mode = args.mode
    ans= args.ans
    if args.ans is not None:
        runner = Playgame(ans=ans)
    else:
        runner = Playgame()

    runner.run(mode=mode)

if __name__ == "__main__":
    main()
