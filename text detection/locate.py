import pyautogui

location = pyautogui.locateOnScreen(
    "C:/Users/asjos/Downloads/boggl/text detection/locate7.png", confidence=0.9
)

locationBot = pyautogui.locateOnScreen(
    "C:/Users/asjos/Downloads/boggl/text detection/locatebot7.png", confidence=0.9
)

# location = pyautogui.locateOnScreen(
#     "E:/Projects/spellcast-solver/text detection/locate.png", confidence=0.9
# )

# locationBot = pyautogui.locateOnScreen(
#     "E:/Projects/spellcast-solver/text detection/locatebot.png", confidence=0.9
# )


pyautogui.moveTo(
    location.left + location.width, location.top + location.height, duration=1
)

import mss.tools

# The screen part to capture  is from (location.left + location.width, location.top + location.height) to (locationBot.left, locationBot.top)

top_left = location.left + location.width
top_right = location.top + location.height

bottom_left = locationBot.left
bottom_right = locationBot.top

with mss.mss() as sct:
    # The screen part to capture
    monitor = {
        "top": int(top_right),
        "left": int(top_left),
        "width": int(bottom_left - top_left),
        "height": int(bottom_right - top_right),
    }
    output = "autoss.png".format(**monitor)

    print(monitor)

    # Grab the data
    sct_img = sct.grab(monitor)

    ## save sct_img to file

    mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
    print(output)

# import mss.tools

# with mss.mss() as sct:
#     # The screen part to capture
#     monitor = {"top": 586, "left": 1912, "width": 310, "height": 316}
#     output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)

#     # Grab the data
#     sct_img = sct.grab(monitor)

#     ## save sct_img to file

#     mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
#     print(output)

#     sct.shot()


# with mss.mss() as sct:
#     monitor = {
#         "top": location.top + location.height,
#         "left": location.left + location.width,
#         "width": locationBot.left - location.left - location.width,
#         "height": locationBot.top - location.top - location.height,
#     }
#     output = "autoss.png".format(**monitor)

#     # Grab the data
#     sct_img = sct.grab(monitor)

#     # Save to the picture file
#     mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
#     print(output)

print(location)

import time

time.sleep(1)

pyautogui.moveTo(locationBot.left, locationBot.top, duration=1)
pyautogui
