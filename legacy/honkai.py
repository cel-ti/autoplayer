import pyautogui
from reldplayer.com.rawconsole import InstanceMeta
from autoplayer.autogui_driver import PyautoguiDriver
from autoplayer.quick import ldplayer9

player = ldplayer9()

player.rawconsole.launchex(
    mnq_name="honkai", apk_package_name="com.miHoYo.bh3global"
)
q = player.rawconsole.query("q['name'] == 'honkai'")  #  type: ignore
q: InstanceMeta = q[0]  # type: ignore
# wait for OK
# autoplayer.sleep(10)

driver = PyautoguiDriver(player.wndmgr.getWnd(q["id"]))
driver.setImgFolder("honkai")

driver.imgWaitAndClick(driver.img("ok"), ignoreError=True)

driver.ocrWaitAndClick("Tap anywhere to")

counter = 0
while True:
    counter += 1
    driver.ocrWaitAndClick("OK", timeout=5, ignoreError=True, regionRatio=(0.7, -0.5))
    driver.ocrWaitAndClick("OK", timeout=5, ignoreError=True, regionRatio=(0.7, -0.5))
    if counter > 3:
        break

# this normalizes me to the home screen
counter = 0
while True:
    counter += 1
    pyautogui.keyDown("esc")
    if counter > 5:
        break

driver.ocrWaitAndClick("Cancel", timeout=5, ignoreError=True)

def goToMission():
    driver.imgWaitAndClick(driver.img("missionIcon"))
    pyautogui.click()
