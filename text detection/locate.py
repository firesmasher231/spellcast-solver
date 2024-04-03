import pyautogui

location = pyautogui.locateOnScreen(
    "E:/Projects/spellcast-solver/text detection/locate.png", confidence=0.9
)

locationBot = pyautogui.locateOnScreen(
    "E:/Projects/spellcast-solver/text detection/locatebot.png", confidence=0.9
)


pyautogui.moveTo(
    location.left + location.width, location.top + location.height, duration=1
)

print(location)

import time

time.sleep(1)

pyautogui.moveTo(locationBot.left, locationBot.top, duration=1)
