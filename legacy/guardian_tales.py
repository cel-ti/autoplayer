
from autoplayer.quick import ldplayer9
from reldplayer.com.rawconsole import InstanceMeta


ldplayer9().rawconsole.launchex(
    mnq_name="guardian_tales", apk_package_name="com.kakaogames.gdts"
)

#autoplayer.sleep(15)

instance : InstanceMeta = ldplayer9().rawconsole.query("q['name'] == 'guardian_tales'")[0]

guardian = ldplayer9().wndmgr.getWnd(instance["id"])

guardian.maximize()

driver = PyautoguiDriver(guardian)
driver.setImgFolder("guardian_tales")
"""

# enter game
driver.clickCenter()

# daily attendence
driver.ocrWaitAndClick("Receive reward", regionRatio=(0.7, -0.5), ignoreError=True)
driver.ocrWaitAndClick("Confirm", regionRatio=(0.7, -0.5), ignoreError=True)

def exitToLobby():
    # repeat key
    driver.repeatKey("esc", 5, 0.5)
    driver.ocrWaitAndClick("Cancel", regionRatio=(1, -0.5), ignoreError=True)
    guardian.maximize()

exitToLobby()

# mail
driver.clickCenterBounding((0.25, 0.2))
driver.ocrWaitAndClick("Receive", regionRatio=(0.5, -0.2))
exitToLobby()"""

# rift
#driver.clickCenterBounding((-0.3, -0.3))
driver.ocrWaitAndClick("Rift", regionRatio=(-0.1, 1))
driver.imgWaitAndClick(driver.img(""))
pass