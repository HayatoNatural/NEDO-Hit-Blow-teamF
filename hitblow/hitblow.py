import argparse
from numberguess import Numberguess

def get_parser() -> argparse.Namespace:
    """コマンドライン引数を解析したものを持つ

    """
    parser = argparse.ArgumentParser(description="Hit&Blow, 数当てゲーム")
    parser.add_argument("--max_count",default=250)
    parser.add_argument("--ans")
    parser.add_argument("--mode",default="auto")
    args = parser.parse_args()
    return args

def main() -> None:
    """数当てゲームのメイン
    """
    args = get_parser()
    mode = args.mode
    max_count = int(args.max_count)
    ans= args.ans
    if args.ans is not None:
        runner = Numberguess(max_count=max_count,ans=ans)
    else:
        runner = Numberguess(max_count=max_count)

    runner.run(mode=mode)
    print(runner.list_where_num_is)

if __name__ == "__main__":
    main()
