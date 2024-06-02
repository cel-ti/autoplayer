from time import sleep

import pyautogui
from autoplayer.autogui_driver import PyautoguiDriver
from autoplayer.quick import ldplayer9

player = ldplayer9()
tofins = player.rawconsole.query("q['name'].startswith('tof.')", True)
tofmain = player.rawconsole.query("q['name'] == 'tof.main'", True)[0]
player.synchronizer.setq(tofins, tofmain)
player.console.launchex(apk_package_name="com.levelinfinite.hotta.gp")
sleep(20)
player.wndmgr.gridOrientation(gridStr="2X2")

tofmainwnd = player.wndmgr.getWnd(tofmain)

driver = PyautoguiDriver(tofmainwnd)
driver.setImgFolder("asset/tof")
try:
    driver.wnd.activate()
except: #noqa
    pass
with pyautogui.hold("ctrl"):
    pyautogui.press("9")

# sign in
driver.imgWaitAndClick(driver.img("close"), regionRatio=(0.5, 0.5))
driver.clickCenter()

# quit all
input("Press any key when done")
player.console.quit()