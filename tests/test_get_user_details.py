import sys
from sys import path

from requests.sessions import _Data

path.append("/home/cwang/vscode_savings/NEDO-Hit-Blow-teamF/hitblow_for_online_F2")
from hitblow_for_online_F2.hitblow_for_F2 import main, get_parser
from hitblow_for_online_F2.setup_and_play_game_for_F2 import Playgame

import pytest


def test_main() -> None:
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

    data=runner.run(mode=mode)

    assert data("hit")==5
    assert data("state")==3