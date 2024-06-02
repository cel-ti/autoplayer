from functools import cache as _cache
import os
from dotenv import load_dotenv
from time import sleep
from zrcl3_uses.automation import (
    AutoToken, 
    waitFor, 
    repeatWith, 
    activate_wnd as activateWnd
)
load_dotenv()

LDPLAYER_PATH = os.environ.get("LDPLAYER_PATH", None)
LDPLAYER9_PATH = os.environ.get("LDPLAYER9_PATH", None)
LDPLAYER4_PATH = os.environ.get("LDPLAYER4_PATH", None)

@_cache
def ldplayer9():
    import reldplayer
    path = LDPLAYER9_PATH if LDPLAYER9_PATH else LDPLAYER_PATH
    if not path:
        return None
    return reldplayer.Player(
        reldplayer.PlayerConfig(path)
    )

@_cache
def ldplayer4():
    import reldplayer
    path = LDPLAYER4_PATH if LDPLAYER4_PATH else LDPLAYER_PATH
    if not path:
        return None
    return reldplayer.Player(
        reldplayer.PlayerConfig(path)
    )


