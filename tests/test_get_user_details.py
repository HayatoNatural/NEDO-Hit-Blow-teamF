import sys
import pytest
from hitblow_for_online_F2.setup_and_play_game_for_F2 import Playgame


sys.path.append("/home/cwang/vscode_savings/NEDO-Hit-Blow-teamF/hitblow_for_online_F2")
sys.path.append("/home/cwang/vscode_savings/NEDO-Hit-Blow-teamF/hitblow")

def test_main() ->None:
    """Hit&Blowのメイン
    """
    """""
    args = parse_args()
    mode = args.mode
    room_id = args.roomid
    ans= args.ans
    """
    runner = Playgame(ans=None,room_id=6010)
    data=runner.run("auto")

    assert data["hit"]==5
    assert data["state"]==3

# python -m pytest tests/