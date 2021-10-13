import sys

from PIL.Image import NONE
from hitblow.Numberguess3 import main,Numberguess2


sys.path.append("/home/cwang/vscode_savings/New_path/NEDO-Hit-Blow-teamF/hitblow")

def test_main() ->None:
    """Hit&Blowのメイン
    """
    """""
    args = parse_args()
    mode = args.mode
    room_id = args.roomid
    ans= args.ans
    """
    ans=None
    if ans is not None:
        runner = Numberguess2(ans=ans)
    else:
        runner = Numberguess2()
    digits,history=runner._play_game_auto()

    assert digits==5

# python -m pytest tests/